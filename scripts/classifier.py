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
    for idx, r in enumerate(YOUT):
        result.append((r, pre_y[idx]))

    conf = confusion(result)
    print(conf)

    result = naiveBayes(svc, X, Y, XIN, YOUT)
    svm_con = confusion(result)
    result = naiveBayes(GaussianNB(), X, Y, XIN, YOUT)
    naiv_con = confusion(result)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    result = naiveBayes(clf, X, Y, XIN, YOUT)
    ccn_con = confusion(result)

    new_days = open("confunsion.csv", 'w')
    X_older = X
    XIN_older = XIN
    lenAttribute = len(X[0])
    for k in range(1, lenAttribute + 1):
        print("\n+++++++   {0}    ++++++++++\n".format(k))
        X = [x[0:k-1] + x[k:] for x in X_older]
        XIN = [y[0:k-1] + y[k:] for y in XIN_older]


        print("svm Test")
        conf0 = svm_con
        result = naiveBayes(svc, X, Y, XIN, YOUT)
        conf = confusion(result)
        print(conf["TPR"], conf["FPR"], conf["TNR"], conf["FNR"], conf["ACC"], conf["F1"])
        print("delta")
        print(conf0["TPR"] - conf["TPR"], conf0["FPR"] - conf["FPR"], conf0["TNR"]-conf["TNR"], conf0["FNR"] - conf["FNR"], conf0["FNR"] - conf["FNR"], conf0["F1"] - conf["F1"])
        print("{0},{1},{2},{3},{4},{5}".format(conf0["TPR"] - conf["TPR"], conf0["FPR"] - conf["FPR"], conf0["TNR"]-conf["TNR"], conf0["FNR"] - conf["FNR"], conf0["FNR"] - conf["FNR"], conf0["F1"] - conf["F1"]))

        new_days.write()


        print("Naive")
        conf0 = naiv_con
        result = naiveBayes(GaussianNB(), X, Y, XIN, YOUT)
        conf = confusion(result)
        print(conf["TPR"],conf["FPR"],conf["TNR"],conf["FNR"],conf["ACC"],conf["F1"])
        print("delta")
        print(conf0["TPR"] - conf["TPR"], conf0["FPR"] - conf["FPR"], conf0["TNR"]-conf["TNR"], conf0["FNR"] - conf["FNR"], conf0["FNR"] - conf["FNR"], conf0["F1"] - conf["F1"])


        #print(conf)
        print("MLP")
        conf0 = ccn_con
        clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes = (5, 2), random_state = 1)
        result = naiveBayes(clf, X, Y, XIN, YOUT)
        conf = confusion(result)
        #print(conf)
        print(conf["TPR"],conf["FPR"],conf["TNR"],conf["FNR"],conf["ACC"],conf["F1"])
        print("delta")
        print(conf0["TPR"] - conf["TPR"], conf0["FPR"] - conf["FPR"], conf0["TNR"]-conf["TNR"], conf0["FNR"] - conf["FNR"], conf0["FNR"] - conf["FNR"], conf0["F1"] - conf["F1"])




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
