import re
from gensim.models.phrases import Phrases, Phraser

try:
    from nltk.corpus import stopwords
    # from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

def remove_stop_words(string):
    if not NLTK_AVAILABLE:
        raise UserWarning("Please install nltk to make use of stop_words")

    stop_words = set(stopwords.words('english'))

    words = string.split()


    unstopped = [w for w in words if not w in stop_words]

    return " ".join(unstopped)

def filter_empty(string):
    """
    Removes unused spaces from string

    >>> filter_empty("data a  a   a ")
    'data a a a'
    """

    content = string.split()
    content = [filter(lambda  x : x != "", s) for s in content]

    return " ".join(content)

def remove_non_alpha_chars(word):
    word = re.sub("\S*\d\S*", "", word).strip()
    word = re.sub('[^A-Za-z]', '', word).strip()

    return word

def clean_raw_text_from_file(file_name, min_length=0):
    with open(file_name) as f:
        content = f.readlines()
    content = map(lambda x : normalize_text(x), content)
    content = filter(lambda x: len(x) > min_length, content)

    return content

def list_of_strings_to_list_of_lists(content):
    return [s.split() for s in content]


def phrasing_sentences(sentences):
    phrases_bi = Phrases(sentences, min_count=5, threshold=1)
    bigram = Phraser(phrases_bi)
    sentences = map(lambda x: x, bigram[sentences])
    phrases_tri = Phrases(sentences, min_count=5, threshold=1)
    trigram = Phraser(phrases_tri)
    return map(lambda x: x, trigram[sentences])


# An alternative short hand
def normalize_text(text):
    """
    Normalizes a string.
    The string is lowercased and all non-alphanumeric characters are removed.

    >>> normalize("already normalized")
    'already normalized'
    >>> normalize("This is a fancy title / with subtitle ")
    'this is a fancy title with subtitle'
    >>> normalize("#@$~(@ $*This has fancy \\n symbols in it \\n")
    'this has fancy symbols in it'
    >>> normalize("Oh no a ton of special symbols: $*#@(@()!")
    'oh no a ton of special symbols'
    >>> normalize("A (2009) +B (2008)")
    'a 2009 b 2008'
    >>> normalize("1238912839")
    '1238912839'
    >>> normalize("#$@(*$(@#$*(")
    ''
    >>> normalize("Now$ this$ =is= a $*#(ing crazy string !!@)# check")
    'now this is a ing crazy string check'
    >>> normalize("Also commata, and other punctuation... is not alpha-numeric")
    'also commata and other punctuation is not alphanumeric'
    >>> normalize(("This goes over\\n" "Two Lines"))
    'this goes over two lines'
    >>> normalize('')
    ''
    """
    return ' '.join(filter(None, (''.join(c for c in w if c.isalnum())
                                  for w in text.lower().split())))




