from nltk.corpus import brown
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

stopWords = set ([w.upper() for w in stopwords.words('english') ])
ps = PorterStemmer()

def run():
    pass


def clean(content):
    pass

def preprocess(content):
    context =  content.split("---------------------- Forwarded",1)[0]
    context = context.upper()

    words = word_tokenize(context)
    wordsStopped = []

    all_stops = stopWords | set(string.punctuation)
    for w in words:
        if w not in all_stops:
            wordsStopped.append(w)

    wordsStemed = [ps.stem(word) for word in wordsStopped]
    return wordsStemed

def processStopWord(content):
    context =  content.split("---------------------- Forwarded",1)[0]
    context = context.lower()

    words = word_tokenize(context)
    wordsStopped = []

    all_stops = stopWords | set(string.punctuation)
    for w in words:
        if w not in all_stops:
            wordsStopped.append(w)
    return wordsStopped


def get_stemmed_content(content):
    return preprocess(content)

