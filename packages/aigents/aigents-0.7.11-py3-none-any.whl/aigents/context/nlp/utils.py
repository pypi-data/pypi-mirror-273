import re
import nltk
from nltk.corpus import stopwords
from collections import Counter


def clean_lines_and_spaces(text):
    text = text.replace("\n", " ")
    text = text.replace("\\n", " ")
    text = text.replace("  ", " ")
    text = text.replace("  ", " ")
    return text

def clean_text(text):
    """
    Sanitizes the input text by removing special characters (excluding spaces,
    digits, and alphabets),
    bullet points (•), and extra spaces. Periods are retained in the sanitized
    text.

    Parameters
    ----------
    text : str
        The text to be sanitized.

    Returns
    -------
    str
        The sanitized text without special characters and extra spaces,
        but with periods, colons and semi-colons retained.

    Examples
    --------
    >>> text_to_sanitize = \"\"\"
    ...     Hello! This is a sample text with special characters: @#$%^&*(),
    ...     bullet points •, extra spaces, and new lines.
    ...
    ...     The text will be sanitized to remove all these elements.
    ... \"\"\"
    >>> sanitized_text = sanitize_text(text_to_sanitize)
    >>> print(sanitized_text)
    Hello This is a sample text with special characters bullet points extra spaces and new lines. The text will be sanitized to remove all these elements.
    """
    text = re.sub(r'[^\w\s.;,\'\"]', '', text)
    text = clean_lines_and_spaces(text)
    text = text.replace('•', '')
    text = text.strip()
    return text


def deep_clean(text,
               language="english",
               n_grams_number=20,
               n_grams_tolerance=2):
    """
    This function cleans a text string based on various cleaning steps.

    Args:
        text: The text string to be cleaned.
        language: The language of the text (default: 'english').

    Returns:
        A cleaned text string.
    """

    # Lowercase the text
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r"<[^>]*>", "", text)
    # Fixing broken words at line breaks
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n-', '', text)
    # Replace remaining newlines with space for continuous reading:
    text = re.sub(r'\n', ' ', text)

    # Remove punctuation
    text = re.sub(r"[^\w\s#]", "", text)

    # Optionally remove stopwords (for languages with stopword lists)
    if language in stopwords.words(language):
        stop_words = stopwords.words(language)
        text = [word for word in text.split() if word not in stop_words]
        text = " ".join(text)

    # Perform stemming and lemmatization (using NLTK)
    stemmer = nltk.stem.PorterStemmer()
    text = stemmer.stem(text)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    text = lemmatizer.lemmatize(text)
    
    # N-gram-based repetition removal
    ngrams = Counter(nltk.ngrams(text.split(), n_grams_number))
    repeated_ngrams = [
        ngram for ngram, count in ngrams.items() if count > n_grams_tolerance
    ]

    for ngram in repeated_ngrams:
        text = text.replace(' '.join(ngram), '')

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text
