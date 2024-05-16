import re
import logging

logger = logging.getLogger(__name__)

def clue_tokenize(text, debug=False):
    quotes_regex = r'(?:(\"[^"]*\")\s+[A-Z])|(?:(\"[^"]*\")\.)|(\"[^"]*\")' # matches double quotes
    """
    (?:(\"[^"]*\")\s+[A-Z])
        quotes followed by whitespace then a capital letter ("ending quote")
    (?:(\"[^"]*\")\.) quotes followed by a period. Some quotes like this do end sentences, but
        we do not count them as such because "ending quotes" have a period inserted after the
        temporary token so sent_tokenize splits on it. Since there is already a period here,
        we do not need to add a period.
    (\"[^"]*\") other kinds of quotes (e.g. inline quotes)
    """
    parentheses_regex = r'(\(.*?\))|(\[.*?\])|(\{.*?\})' # matches parentheses, brackets, and braces
    
    honorifics = ["Mr", "Ms", "Mrs", "Jr", "Sr",
              "Sen", "Pres", "Gov", "Gen",
              "Dr", "Rev", "Hon", "Prof", "Asst",
              "Gen", "Lt", "Col", "Maj", "Sgt", "Cdr", "Capt",
              "No", "Mt", "Ave", "St",
              "Fr", "Vp", "Ofc", "Pr", "Br", "Rep",
              "Mme", "Mlle", "Hr", "Fr"]
    
    other_abbrevs = ["et al", "v",
                     "Corp", "Ltd", "Assoc", "Co", "Inc"]
    
    abbreviations = honorifics + other_abbrevs
    
    abbreviations_pattern = r'(?:' + '|'.join(f'{abbr}.' for abbr in abbreviations) + r'\.)'
    misc_regex = f'({abbreviations_pattern}' + r' [^\s.]+)|((?:[A-HJ-UW-Z]+\.\s?)+)' # matches troublesome abbreviations

    quotes_tup_list = re.findall(quotes_regex, text)
    paren_tup_list = re.findall(parentheses_regex, text)
    misc_tup_list = re.findall(misc_regex, text)
    trouble_strs = quotes_tup_list + paren_tup_list + misc_tup_list
    quotes = [next((s for s in tup if s), "") for tup in quotes_tup_list]
    if debug: logger.debug(trouble_strs)

    is_ending_quote = [tup[0] != '' for tup in quotes_tup_list] + len(paren_tup_list + misc_tup_list) * [False]
    if debug: logger.debug(is_ending_quote)

    trouble_strs = [next(filter(lambda x: x != '', tup)) for tup in trouble_strs]
    if debug: logger.debug(trouble_strs)

    temp_tok_text = text

    for i, s in enumerate(trouble_strs):
        if is_ending_quote[i]:
            temp_tok_text = temp_tok_text.replace(s, f"[TEMP_TOK_{i}].", 1)
        else:
            temp_tok_text = temp_tok_text.replace(s, f"[TEMP_TOK_{i}]", 1)

    sents = re.split(r'(?<=[?.!])\s+', temp_tok_text)
    if debug: logger.debug(sents)

    for i, sent in enumerate(sents):
        for temp_tok in re.findall(r'\[TEMP_TOK_(\d+)\]\.?', sent):
            num_tok = 0

            try:
                num_tok = int(temp_tok)
            except:
                logger.debug("NOT INT")
                logger.debug(text)
                logger.debug(temp_tok)
                logger.debug(trouble_strs)
                logger.debug(is_ending_quote)
                pass

            if num_tok >= len(is_ending_quote):
                logger.debug("out of bounds")
                logger.debug(text)
                logger.debug(num_tok)
                logger.debug(is_ending_quote)
                pass

            if is_ending_quote[num_tok]:
                sent = sent.replace(f"[TEMP_TOK_{num_tok}].", trouble_strs[num_tok])
            else:
                sent = sent.replace(f"[TEMP_TOK_{num_tok}]", trouble_strs[num_tok])
        sents[i] = sent

    return sents