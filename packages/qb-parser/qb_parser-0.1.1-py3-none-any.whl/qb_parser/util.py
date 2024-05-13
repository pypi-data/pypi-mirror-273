import re

def extract_braced_text(text):
    """ Extracts text enclosed within curly braces from the input string.
    If no braced text is found, it returns the input string without any change.
    
    Args:
        input_string (str): The input string to process.
        
    Returns:
        str: The concatenated braced text or the input string unchanged.
    """
    matches = re.findall(r'(?<={)[^}]*', text)
    
    if matches:
        return ' '.join(matches)
    else:
        return text

def remove_braces(text: str) -> str:
        """Removes HTML tags from a string."""
        return re.sub(r'[{}]', '', text)

def extract_key_words(text):
    """ Get all words which are partially or wholly enclosed in curly braces.
    
    Args:
        input_string (str): The input string to process.
        
    Returns:
        str: A string containing all words found in curly braces or the whole word, cleaned of any remaining braces.
    """
    required_words = extract_braced_text(text).split()
    
    # Filtering and collecting words inside or partially inside braces
    filtered_words = [
        remove_braces(word) for word in text.split()
        if re.search(r'{|}', word) or word in required_words
    ]
    
    return ' '.join(filtered_words)

def extract_quotes(text: str) -> str:
    """Extracts the text in quotes from a given string. Returns the extracted quotes or the original string without HTML tags."""
    matches = re.findall(r'(?<=["])[^"]*(?=["])', text)
    if matches:
        return remove_braces(' '.join(matches))
    return remove_braces(text)

def get_abbreviation(text: str) -> str:
    """Get the abbreviation of a string by taking the first letter of each word. E.g., 'World Health Organization' becomes 'WHO'."""
    words = re.sub(r'<[^>]*>', '', text).split()
    return ''.join(word[0] for word in words if word)

def remove_parentheses_and_brackets(text: str) -> str:
    """Removes parentheses and square brackets from a string."""
    text = re.sub(r'\([^)]*\)', '', text)
    return re.sub(r'\[[^\]]*\]', '', text)

def remove_punctuation(text: str) -> str:
    """Removes punctuation from a string."""
    return re.sub(r'[.,!;:\'"\\/?@#$%^&*_~’]', '', text)

def replace_special_substrings(text: str) -> str:
    # Replace \(s\) with 's'
    text = re.sub(r'\(s\)', 's', text)
    
    # Replace all types of dashes with a standard hyphen
    text = re.sub(r'\u2013|\u2014|\u2015|\u2010', '-', text)
    
    return text

def replace_special_characters(text: str) -> str:
    # Normalize to NFD (Normalization Form Decomposition)
    # normalized_string = unicodedata.normalize('NFD', input_string)
    
    # Remove combining characters (diacritical marks)
    # without_combining = re.sub(r'[\u0300-\u036f]', '', normalized_string)
    
    # Replace various types of quotation marks with standard quotes
    return re.sub(r'["“‟❝”❞]', '"', text)