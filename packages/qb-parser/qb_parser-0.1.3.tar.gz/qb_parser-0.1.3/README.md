# qb-parser Documentation

qb-parser is a Python package for parsing the questions and answerlines in quizbowl. The answerline parser *heavily* borrows from [qbreader's qb-answer-checker](https://github.com/qbreader/qb-answer-checker/tree/main).

## Installation

```
pip install qb-parser
```

## Usage

### clue_tokenize()
`clue_tokenize()` splits quizbowl questions into a list of clues just like [nltk's `sent_toknize()`](https://www.nltk.org/api/nltk.tokenize.sent_tokenize.html). It was written because the use of quotes and many periods (e.g. "Symphony No. 9") make quizbowl questions difficult for `sent_tokenize()`.

### AnswerLineParser

The `AnswerLineParser` is designed to parse answerlines containing directives and answers, and returning an `Answer` object. The answerline parser *heavily* borrows from [qbreader's qb-answer-checker](https://github.com/qbreader/qb-answer-checker/tree/main).

#### `parse_answerline(self, answerline: str) -> Answer`
- **Parameters:**
  - `answerline`: A string containing directives and bracketed answers.
- **Returns:** An `Answer` object containing organized directives and answers.

#### Example Usage

```python
from qb_parser import AnswerLineParser
parser = AnswerLineParser()
answer = parser.parse_answerline("Adventure [accept {Microsoft Adventure} or {Colossal Cave Adventure}; accept {graphic adventures}; prompt on {graphic} with 'what other word is in the name of that genre?']")
print(answer)
```

#### Output
```
(<Directive.ACCEPT: 'accept'>, [('Adventure', ''), ('Microsoft Adventure', ''), ('Colossal Cave Adventure', ''), ('graphic adventures', ''), ('graphic adventure', '')])
(<Directive.REJECT: 'reject'>, [])
(<Directive.REGULAR_PROMPT: 'regular_prompt'>, [('graphic', 'what other word is in the name of that genre?')])
(<Directive.ANTIPROMPT: 'antiprompt'>, [])
```

### Answer
The `Answer` class describes the answer for a quizbowl question. Internally, it uses a `directive_map` that, given a `Directive` (e.g. `Directive.ACCEPT`), produces a `AnswerAction`. `AnswerAction` contains a list of `SingleAnswer`s that contain the `answer_text` and other useful properties like `exact_directed_prompt`.


#### Fields
- `directive_map`: A dictionary mapping `Directive` types to `AnswerAction` objects.

#### Methods

- `getAnswerAction(self, directive: Directive) -> AnswerAction`
  - Retrieves an `AnswerAction` based on the given `Directive`.
  - **Parameters:**
    - `directive`: A `Directive` enum value.
  - **Raises:**
    - `ValueError` if the directive is not found.

- `addAnswerAction(self, answerAction: AnswerAction)`
  - Adds an `AnswerAction` to the corresponding directive in `directive_map`.
  - **Parameters:**
    - `answerAction`: An `AnswerAction` object to add.
  - **Raises:**
    - `RuntimeError` if the directive is invalid.
