from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from itertools import chain

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."


doc_a = "Aapple Aapple Aapple"
doc_b = "Dog Dog Dog"
doc_c = "Bird Bird Bird"
doc_d = "July July July"
doc_e = "windows windows windows"

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

doc_target = [doc_a]



# loop through document list
def getCorpus(doc_set):
    # list for tokenized documents in loop
    texts = []
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)
    return texts

def getTopics(documents,num_topics):
    texts = getCorpus(documents)
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    tardoc = [dictionary.doc2bow(text) for text in getCorpus(doc_target)]
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics, id2word=dictionary, passes=20)

    print("topics in this cropus")
    for topic in ldamodel.print_topics(num_words=3):
        print(topic)



    # Assinging the topics to the document in corpus
    lda_corpus = ldamodel[corpus]

    # Find the threshold, let's set the threshold to be 1/#clusters,
    # To prove that the threshold is sane, we average the sum of all probabilities:
    scores = list(chain(*[[score for topic_id,score in topic] \
                     for topic in [doc for doc in lda_corpus]]))
    threshold = sum(scores)/len(scores)
    print(threshold)

#for index, item in enumerate(items):
#    print(index, item)


    cluster1 = [j for i,j in zip(lda_corpus,doc_set) if i[0][1] > threshold]
    cluster2 = [j for i,j in zip(lda_corpus,doc_set) if i[1][1] > threshold]
    cluster3 = [j for i,j in zip(lda_corpus,doc_set) if i[2][1] > threshold]

    print(cluster1)
    print(cluster2)
    print(cluster3)

    #print(ldamodel[tardoc])


getTopics(doc_set,5)
