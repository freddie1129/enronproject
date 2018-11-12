import numpy as np
#import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import ComplementNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier

import numpy as np
from enron.models import Person
from scripts.emailconst import mailConstant
from django.db.models import Q
import math

def run():
    person = Person.objects.filter(Q(type=mailConstant.analysis_type_training), ~Q(scale_level=None), ~Q(diversity=None)).order_by("scale_level")
    size = person.count()
    l_index = math.floor(size / 5)
    h_index = size -  l_index
    person_l = person[:l_index]
    person_h = person[h_index:]
    dataset_l = [[p.diversity,p.density,p.ratio,p.time_ratio,p.senti_level,p.topic_change] for p in person_l ]
    result_l = [True] * len(dataset_l)
    dataset_h = [[p.diversity,p.density,p.ratio,p.time_ratio,p.senti_level,p.topic_change] for p in person_h ]
    result_h = [False] * len(dataset_h)
    X = dataset_l + dataset_h
    Y = result_l + result_h


    C = 1.0 # SVM regularization parameter,poly
    svc = svm.SVC(kernel='linear',C=1).fit(X, Y)
    person = Person.objects.filter(Q(type=mailConstant.analysis_type_testing), ~Q(scale_level=None), ~Q(diversity=None)).order_by("scale_level")
    size = person.count()
    l_index = math.floor(size / 5)
    h_index = size - l_index
    person_l = person[:l_index]
    person_h = person[h_index:]
    dataset_l = [[p.diversity, p.density, p.ratio, p.time_ratio, p.senti_level, p.topic_change] for p in person_l ]
    result_l = [True] * len(dataset_l)
    dataset_h = [[p.diversity, p.density, p.ratio, p.time_ratio, p.senti_level, p.topic_change] for p in person_h ]
    result_h = [False] * len(dataset_h)
    XIN = dataset_l + dataset_h
    YOUT = result_l + result_h
    pre_y = svc.predict(XIN)

    print("++++++++++++++++++++++++++++++++++++++++++++")
    print(pre_y)
    print("++++++++++++++++++++++++++++++++++++++++++++")

    result = []
    for idx,r in enumerate(YOUT):
        result.append((r,pre_y[idx]))

    conf = confusion(result)
    print(conf)




    print("GaussianNB Naive Beyes Classifier Test")
    result = naiveBayes(GaussianNB(),X,Y,XIN,YOUT)
    conf = confusion(result)
    print(conf)

    print("BernoulliNB Naive Beyes Classifier Test")
    result = naiveBayes(BernoulliNB(),X,Y,XIN,YOUT)
    conf = confusion(result)
    print(conf)

    print("MultinomialNB Naive Beyes Classifier Test")
    result = naiveBayes(MultinomialNB(),X,Y,XIN,YOUT)
    conf = confusion(result)
    print(conf)

    print("ComplementNB Naive Beyes Classifier Test")
    result = naiveBayes(ComplementNB(),X,Y,XIN,YOUT)
    conf = confusion(result)
    print(conf)

    print("MLP classifier")
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
    result = naiveBayes(clf, X, Y, XIN, YOUT)

    conf = confusion(result)
    print(conf)


def reverse(list):
    for index, value in enumerate(list):
        list[index] = not list[index]
    return list



def naiveBayes(classifier,x_t,y_t,x_testing,y_testing):
    # Create a Gaussian Classifier
    # model = BernoulliNB()

    # Train the model using the training sets
    classifier.fit(x_t, y_t)

    # Predict Output
    yp= classifier.predict(x_testing)

    result = []
    for idx, r in enumerate(y_testing):
        result.append((r, yp[idx]))
    #print(result)
    return result

def confusion(result):
    P = len([x for x in result if x[0]])
    N = len([x for x in result if x[0] == False])
    TP = len([x for x in result if x[0] == True and x[1] == True])
    TN = len([x for x in result if x[0] == False and x[1] == False])
    FP = len([x for x in result if x[0] == False and x[1] == True])
    FN = len([x for x in result if x[0] == True and x[1] == False])
    TPR = TP / P
    TNR = TN / N
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    FNR = FN / P
    FPR = FP / N    
    FDR = FP / (FP + TP)
    ACC = (TP + TN) / (P + N)
    F1 = 2 * (PPV * TPR) / (PPV + TPR)
    r = {
        "P":P,
        "N":N,
        "TP":TP,
        "TN":TN,
        "FP":FP,
        "FN":FN,
        "TPR":TPR,
        "TNR":TNR,
        "PPV":PPV,
        "NPV":NPV,
        "FPR":FPR,
	    "FNR":FNR,
        "FDR":FDR,
        "ACC":ACC,
        "F1":F1}
    return r
