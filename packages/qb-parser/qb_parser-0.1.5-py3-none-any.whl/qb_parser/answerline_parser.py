import re
from enum import  Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .util import *

class Directive(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    PROMPT = "prompt"
    REGULAR_PROMPT = "regular_prompt"
    ANTIPROMPT = "antiprompt"


SEARCH_STRS: Dict[Directive, List[str]] = {
    Directive.ACCEPT: ["also accept", "accept", "or"],
    Directive.REJECT: ["do not accept or prompt on", "do not accept", "reject"],
    Directive.PROMPT: ["antiprompt on", "anti-prompt on", "antiprompt", "anti-prompt", "prompt on", "prompt"],
    Directive.REGULAR_PROMPT: ["prompt on", "prompt"],
    Directive.ANTIPROMPT: ["antiprompt on", "anti-prompt on", "antiprompt", "anti-prompt"]
}

ALL_SEARCH_STRS: List[str] = SEARCH_STRS[Directive.PROMPT] + SEARCH_STRS[Directive.REJECT] + SEARCH_STRS[Directive.ACCEPT]

@dataclass
class SingleAnswer:
    answer_text: str
    before_text: str = ""
    before_index: int = -1
    exact_directed_prompt: str = ""
    

@dataclass
class AnswerAction:
    """The action (directive) for a given answer."""
    directive: Directive
    answers: List[SingleAnswer] = None

    def __post_init__(self):
        if self.answers is None:
            self.answers = []

    def getDirective(self) -> Directive:
        return self.directive
    
    def getAnswerList(self) -> List[SingleAnswer]:
        return self.answers
    
    def addToAnswerList(self, answers: List[SingleAnswer]) -> None:
        for singleAnswer in answers:
            if (singleAnswer not in self.answers): self.answers.append(singleAnswer)
    
    def __str__(self):
        return f"{type(self.directive)} {self.answers}"
    
    def __repr__(self):
        return f"{type(self.directive)} {self.answers}"


@dataclass
class Answer:
    directive_map: Dict[Directive, AnswerAction] = field(default_factory=lambda: {
        Directive.ACCEPT: AnswerAction(directive=Directive.ACCEPT),
        Directive.REJECT: AnswerAction(directive=Directive.REJECT),
        Directive.REGULAR_PROMPT: AnswerAction(directive=Directive.REGULAR_PROMPT),
        Directive.ANTIPROMPT: AnswerAction(directive=Directive.ANTIPROMPT),
    })

    def addAnswerAction(self, answerAction: AnswerAction):
        directive = answerAction.getDirective()
        if directive in self.directive_map:
            self.directive_map[directive].addToAnswerList(answerAction.getAnswerList())
        else:
            raise RuntimeError("Invalid directive type", directive)

    def getAnswerAction(self, directive: Directive) -> AnswerAction:
        if directive in self.directive_map:
            return self.directive_map[directive]
        else:
            raise ValueError("Directive not found:", directive)
    
    def __repr__(self) -> str:
        return "\n".join(f"{dir, [(a.answer_text, a.exact_directed_prompt) for a in answer.getAnswerList()]}" for dir, answer in self.directive_map.items())

class AnswerLineParser:

    def split_main_answer(self, string) -> Tuple[str, str]:
        brackets_sub_answerline: list = re.findall(r'(?<=\[)[^\]]*(?=\])', string)
        parentheses_sub_answerline: list = re.findall(r'(?<=\()[^)]*(?=\))', string)

        main_answerline: str = remove_parentheses_and_brackets(string)
        brackets_sub_answerline: str = brackets_sub_answerline.pop() if brackets_sub_answerline else ''
        parentheses_sub_answerline: str = parentheses_sub_answerline.pop() if parentheses_sub_answerline else ''

        if brackets_sub_answerline:
            return main_answerline, brackets_sub_answerline

        for directive in ALL_SEARCH_STRS:
            if parentheses_sub_answerline.startswith(directive):
                return main_answerline, parentheses_sub_answerline

        return main_answerline, ''

    def split_answerline_into_clauses(self, string):
        return [token.strip() for token in string.split(';')]
    
    def getDirectiveType(self, clause: str) -> Directive:
        for directiveType in [Directive.REJECT, Directive.REGULAR_PROMPT, Directive.ANTIPROMPT, Directive.ACCEPT]:
            for searchString in SEARCH_STRS[directiveType]:
                if clause.startswith(searchString):
                    return directiveType
            
        return Directive.ACCEPT
    
    def get_possible_cleaned_answers(self, directiveless_clause: str, exact_directed_prompt: str = "") -> List[SingleAnswer]:
        possible_ans_text = [extract_quotes(directiveless_clause),
                            extract_key_words(directiveless_clause),
                            extract_braced_text(directiveless_clause)]
        
        return [SingleAnswer(answer_text=ans_text, exact_directed_prompt=exact_directed_prompt)
                for ans_text in possible_ans_text]

    def split_clause_into_answers(self, clause) -> AnswerAction:
        directive: Directive = self.getDirectiveType(clause)
        exact_directed_prompt: str = ""

        # Find if there is a specific way to read the prompt
        # Example: "prompt on Map by asking 'what kind of Map?'"

        if (re.search(r'(accept either)', clause, re.IGNORECASE) or
            re.search(r'(accept any)', clause, re.IGNORECASE) or
            re.search(r'prompt on (a )?partial', clause, re.IGNORECASE)):
            return AnswerAction(directive=directive, answers=[])

        if (directive == Directive.REGULAR_PROMPT or directive == Directive.ANTIPROMPT):
            for key in ['by asking', 'with']:
                index = clause.find(key)
                if index >= 0:
                    exact_directed_prompt = extract_quotes(clause[index+len(key):])
                    clause = clause[:index]
                    break

        # Remove directives
        remove_directive_pattern = r'^(' + '|'.join(ALL_SEARCH_STRS) + r')'
        directiveless_clause = re.sub(remove_directive_pattern, '', clause).strip()

        answers: List[SingleAnswer] = []
        
        #TODO: add "before" parsing
        for ans_text in re.split(r',? or |, ', directiveless_clause):
            if ans_text:
                answers.extend(
                    self.get_possible_cleaned_answers(ans_text, exact_directed_prompt)
                )
                
        answerAction = AnswerAction(directive=directive, answers=answers)

        return answerAction

    def parse_answerline(self, answerline) -> Answer:
        answerline = replace_special_characters(answerline)
        answerline = replace_special_substrings(answerline)

        answer = Answer()

        main_answer, sub_answer = self.split_main_answer(answerline)
        main_answers: List[SingleAnswer] = []

        for possible_ans in main_answer.split(' or '):
            if possible_ans:
                main_answers.extend(
                    self.get_possible_cleaned_answers(possible_ans.strip(), exact_directed_prompt="")
                )
        mainAnswerAction = AnswerAction(directive=Directive.ACCEPT, answers=main_answers)
        answer.addAnswerAction(mainAnswerAction)
        
        clauses = self.split_answerline_into_clauses(sub_answer)
        for clause in clauses:
            if not clause: continue
            answerAction = self.split_clause_into_answers(clause)
            answer.addAnswerAction(answerAction)

        return answer


# Example usage:
# parser = AnswerLineParser()
# parsed_data = parser.parse_answerline("Corpus Juris Civilis [accept Body of Civil Law; accept the Code of Justinian or Justinian’s Code]")
# parsed_data = parser.parse_answerline("realignments [reject \"dealignments\"]")
# parsed_data = parser.parse_answerline("{21} cm line [prompt on the hydrogen line before mention]")
# parsed_data = parser.parse_answerline("Frédéric (François) {Chopin} [or Fryderyk (Franciszek) {Szopen}]")
# parsed_data = parser.parse_answerline("Adventure [accept {Microsoft Adventure} or {Colossal Cave Adventure}; accept {graphic adventure}s; prompt on {graphic} with “what other word is in the name of that genre?”]")
# parsed_data = parser.parse_answerline("defenestration [prompt on “falling”; accept reasonable equivalents like “jumping out of a window” or “being thrown out of a window”; prompt on “suicide”]")
# print(parsed_data)
