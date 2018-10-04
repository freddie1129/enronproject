import spacy
#spacy.load('en')
from spacy.lang.en import English
from gensim import corpora
import nltk

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import gensim
import pickle
import math
import numpy as np

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
    topics_summery = []
    for month in re_list:
        #print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #print("{0},{1},{2},{3}".format(month[0], month[1], len(month[2]), len(month[3])))
        if len(month[2]) != 0:
            text_data = []
            for line in month[3]:
                tokens =  prepare_text_for_lda(line)
                text_data.append(tokens)
            dictionary = corpora.Dictionary(text_data)
            corpus = [dictionary.doc2bow(text) for text in text_data]
            pickle.dump(corpus, open('corpus.pkl', 'wb'))
            dictionary.save('dictionary.gensim')

            NUM_TOPICS = 5
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
            ldamodel.save('model5.gensim')
            topics = ldamodel.print_topics(num_words=5)
            #print(ldamodel.get_topics())
            #print('&&&&&&&&&&&&&&&&&&&')
            topic_array = []
            for topic in topics:
                #topic[1]
                ws = topic[1].split("+")
                dic = []
                for w in ws:
                    s = w.split("*")
                    #dic[s[1].split("\"")[1]] = float(s[0])
                    dic.append ((s[1].split("\"")[1], float(s[0])))
                #print(dic)
                topic_array.append(dic)
            #print(topic_array)

            #sim = gensim.matutils.cossim([], [])
            #print("sim: {0}".format(sim))

            new_doc = str.join(" ",month[3])
            new_doc = prepare_text_for_lda(new_doc)
            new_doc_bow = dictionary.doc2bow(new_doc)
            # print(new_doc_bow)
            v1 = ldamodel.get_document_topics(new_doc_bow)
            topic_main = []
            topic_en = []
            #print(v1)
            for t in v1:
                weight_topic = [(m[0],m[1]*t[1]) for m in topic_array[t[0]]]
                topic_main.append(weight_topic)
                topic_en += weight_topic

            #print(topic_main)
            #print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            #print(topic_en)
            topics_summery.append(topic_en)
            #topics.append(v1)
            #print(v1)
        else:
            #print("**************No Emails in this month*****************")
            topics_summery.append([])
    #print("==========================================================")
    simi = []
    for idx, topic in enumerate(topics_summery[0:-1]):
        next_topic = topics_summery[idx + 1]
        s = gensim.matutils.cossim(topic,next_topic)
        simi.append(s)
        print("Similarity: {0}".format(s))
    ava_simi = np.average(simi)
    print("Avarge Similarity: {0}".format(ava_simi))
    return  ava_simi
    #for t in topics_summery:
    #    print(t)

    #print(topics_summery)