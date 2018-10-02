#import spacy
#spacy.load('en')
from spacy.lang.en import English

parser = English()


def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


import nltk
from nltk.corpus import wordnet as wn


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


from nltk.stem.wordnet import WordNetLemmatizer


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


for w in ['dogs', 'ran', 'discouraged']:
    print(w, get_lemma(w), get_lemma2(w))

en_stop = set(nltk.corpus.stopwords.words('english'))


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


import random


def run():
    text_data = []
    with open('./2.csv') as f:
        for line in f:
            tokens = prepare_text_for_lda(line)
            if random.random() > .99:
                print(tokens)
                text_data.append(tokens)





text_data = []
raw_text = """This rustic lamb casserole is full of flavour, especially if made ahead, and the lamb is meltingly tender. Harissa is a chilli paste with quite a kick; rose harissa, which I prefer to use, is sweeter and less fiery due to the addition of rose petals. I don’t like my food too spicy, so this dish is mild, but if you prefer it hot just add more harissa and good luck!"""
tokens = prepare_text_for_lda(raw_text)
text_data.append(tokens)

import gensim
from gensim import corpora

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
import pickle

pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)
