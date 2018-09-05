from nltk.corpus import brown
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

stopWords = set(stopwords.words('english'))
ps = PorterStemmer()

def run():
    pass


def clean(content):
    pass

def preprocess(content):
    words = word_tokenize(content)
    wordsStopped = []

    for w in words:
        if w not in stopWords:
            wordsStopped.append(w)

    wordsStemed = [ps.stem(word) for word in wordsStopped]
    return wordsStemed
