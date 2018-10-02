import spacy
#spacy.load('en')
from spacy.lang.en import English
from gensim import corpora
import nltk

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import gensim

nltk.download('wordnet')
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))
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







def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma




def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)



def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

import random
def run():
    text_data = []
    with open('dataset.csv') as f:
        idx  = 0
        for line in f:
            if idx < 5:
                tokens = prepare_text_for_lda(line)
                print(tokens)
                text_data.append(tokens)
            else:
                break
            idx += 1

            #if random.random() > .99:
            #    print(tokens)
            #    text_data.append(tokens)

    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')

    import gensim
    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)



def topic(lines):
    text_data = []
    # with open('dataset.csv') as f:
    #     idx  = 0
    #     for line in f:
    #         if idx < 5:
    #             tokens = prepare_text_for_lda(line)
    #             print(tokens)
    #             text_data.append(tokens)
    #         else:
    #             break
    #         idx += 1

    for line in lines:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
        print(tokens)

        #if random.random() > .99:
            #    print(tokens)
            #    text_data.append(tokens)



    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')


    NUM_TOPICS = 6
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")


    topics = []
    for l in lines:
        new_doc = l
        new_doc = prepare_text_for_lda(new_doc)
        new_doc_bow = dictionary.doc2bow(new_doc)
        print(new_doc_bow)
        v1 = ldamodel.get_document_topics(new_doc_bow)
        topics.append(v1)
        #print(v1)

    for idx, topic in enumerate(topics[0:-1]):
        next_topic = topics[idx + 1]
        s = gensim.matutils.cossim(topic,next_topic)
        print("Similarity: {0}".format(s))



def topic_re(re_list):


    lines = [str.join(" ",month[3]) for month in re_list]
    text_data = []
    for line in lines:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
        #print(tokens)

        #if random.random() > .99:
            #    print(tokens)
            #    text_data.append(tokens)



    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')


    NUM_TOPICS = 6
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")


    topics = []
    for idx, l in enumerate(lines):
        print("Topic: start: {0}  end: {1}, email number: {2}".format(re_list[idx][0], re_list[idx][1], len(re_list[idx][2])))
        new_doc = l
        new_doc = prepare_text_for_lda(new_doc)
        new_doc_bow = dictionary.doc2bow(new_doc)
        #print(new_doc_bow)
        v1 = ldamodel.get_document_topics(new_doc_bow)
        topics.append(v1)
        print(v1)

    for idx, topic in enumerate(topics[0:-1]):
        next_topic = topics[idx + 1]
        s = gensim.matutils.cossim(topic,next_topic)
        print("Similarity: {0}".format(s))


def topic_re_V2(re_list):


    lines = [str.join(" ",month[3]) for month in re_list]
    text_data = []
    for line in lines:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
        #print(tokens)

        #if random.random() > .99:
            #    print(tokens)
            #    text_data.append(tokens)



    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    import pickle
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')


    NUM_TOPICS = 6
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        print(topic)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")


    topics = []
    for idx, l in enumerate(lines):
        print("Topic: start: {0}  end: {1}, email number: {2}".format(re_list[idx][0], re_list[idx][1], len(re_list[idx][2])))
        new_doc = l
        new_doc = prepare_text_for_lda(new_doc)
        new_doc_bow = dictionary.doc2bow(new_doc)
        #print(new_doc_bow)
        v1 = ldamodel.get_document_topics(new_doc_bow)
        topics.append(v1)
        print(v1)

    for idx, topic in enumerate(topics[0:-1]):
        next_topic = topics[idx + 1]
        s = gensim.matutils.cossim(topic,next_topic)
        print("Similarity: {0}".format(s))