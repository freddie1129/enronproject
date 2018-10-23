import numpy as np
#import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
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
    result_l = [1] * len(dataset_l)
    dataset_h = [[p.diversity,p.density,p.ratio,p.time_ratio,p.senti_level,p.topic_change] for p in person_h ]
    result_h = [0] * len(dataset_h)
    X = dataset_l + dataset_h
    y = result_l + result_h

    for x in X:
        print(x)

    for i in y:
        print(i)



    C = 1.0 # SVM regularization parameter,poly
    #svc = svm.SVC(kernel='poly', gamma = 'scale',C=1).fit(X, y)
    svc = svm.SVC(kernel='linear',C=1).fit(X, y)



    person = Person.objects.filter(Q(type=mailConstant.analysis_type_testing), ~Q(scale_level=None),~Q(diversity=None)).order_by("scale_level")
    size = person.count()
    l_index = math.floor(size / 5)
    h_index = size -  l_index
    person_l = person[:l_index]
    person_h = person[h_index:]
    dataset_l = [[p.diversity,p.density,p.ratio,p.time_ratio,p.senti_level,p.topic_change] for p in person_l ]
    result_l = [1] * len(dataset_l)
    dataset_h = [[p.diversity,p.density,p.ratio,p.time_ratio,p.senti_level,p.topic_change] for p in person_h ]
    result_h = [0] * len(dataset_h)
    XIN = dataset_l + dataset_h
    YOUT = result_l + result_h
    pre_y = svc.predict(XIN)
    result = []
    for idx,r in enumerate(YOUT):
        result.append(r==pre_y[idx])
        print("{0}: {1},{2},{3}".format(idx,r, pre_y[idx],r == pre_y[idx]))
    print(result)
    a_true = [a for a in result  if a]
    a_false = [a for a in result if not a]
    lt = len(a_true)
    lf = len(a_false)
    print("Correct: {0}, Incorrect： {1}, Total: {2}, Score: {3}".format(lt, lf, lt + lf, lt / (lt + lf)))


    print("\n\nLowest 1/5 strengh level as True")
    print("##############################################")
    #confusion matrix
    P = len(person_l)
    N = len(person_h)
    TP = len([x for x in result[:P] if x])
    TN = len([x for x in result[P:] if x])
    FN = len([x for x in result[:P] if not x])
    FP = len([x for x in result[P:] if not x])

    TPR = TP / P
    TNR = TNR = TN / N
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    FNR = FN / P;
    FDR = FP / (FP + TP)
    ACC = (TP + TN) / (P + N)
    F1 = 2 * (PPV * TPR) / (PPV + TPR)
    print("P={0},N={1},TP={2},TN={3},FN={4},FP={5}".format(P,N,TP,TN,FN,FP))
    print("ACC={0},F1={1}".format(ACC,F1))
    print("##############################################")

    print("\n\nHighest 1/5 strengh level as True")
    print("##############################################")
    # confusion matrix
    P = len(person_h)
    N = len(person_l)
    TN = len([x for x in result[:P] if  x])
    TP = len([x for x in result[P:] if  x])

    FP = len([x for x in result[:P] if not x])
    FN = len([x for x in result[P:] if not x])

    TPR = TP / P
    TNR = TN / N
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    FNR = FN / P
    FDR = FP / (FP + TP)
    ACC = (TP + TN) / (P + N)
    F1 = 2 * (PPV * TPR) / (PPV + TPR)
    print("P={0},N={1},TP={2},TN={3},FN={4},FP={5}".format(P, N, TP, TN, FN, FP))
    print("ACC={0},F1={1}".format(ACC, F1))
    print("##############################################")

    # assigning predictor and target variables
    #x = np.array(
    #    [[-3, 7], [1, 5], [1, 2], [-2, 0], [2, 3], [-4, 0], [-1, 1], [1, 1], [-2, 2], [2, 7], [-4, 1], [-2, 7]])
    #Y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])

    #x = [[-3, 7], [1, 5], [1, 2], [-2, 0], [2, 3], [-4, 0], [-1, 1], [1, 1], [-2, 2], [2, 7], [-4, 1], [-2, 7]]
    #Y = [3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4]

    # Create a Gaussian Classifier
    model = GaussianNB()

    # Train the model using the training sets
    model.fit(X, y)

    # Predict Output
    pre_y = model.predict(XIN)

    result = []
    for idx, r in enumerate(YOUT):
        result.append(r == pre_y[idx])
        #print("{0}: {1},{2},{3}".format(idx, r, pre_y[idx], r == pre_y[idx]))
    #print(result)

    print("\n\nLearn Naive Bayes Lowest 1/5 strengh level as True")
    print("##############################################")
    #confusion matrix
    P = len(person_l)
    N = len(person_h)
    TP = len([x for x in result[:P] if x])
    TN = len([x for x in result[P:] if x])
    FN = len([x for x in result[:P] if not x])
    FP = len([x for x in result[P:] if not x])

    TPR = TP / P
    TNR = TN / N
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    FNR = FN / P
    FDR = FP / (FP + TP)
    ACC = (TP + TN) / (P + N)
    F1 = 2 * (PPV * TPR) / (PPV + TPR)
    print("P={0},N={1},TP={2},TN={3},FN={4},FP={5}".format(P,N,TP,TN,FN,FP))
    print("ACC={0},F1={1}".format(ACC,F1))
    print("##############################################")

    print("\n\nLearn Naive Bayes Highest 1/5 strengh level as True")
    print("##############################################")
    # confusion matrix
    P = len(person_h)
    N = len(person_l)
    TN = len([x for x in result[:P] if  x])
    TP = len([x for x in result[P:] if  x])

    FP = len([x for x in result[:P] if not x])
    FN = len([x for x in result[P:] if not x])

    TPR = TP / P
    TNR = TNR = TN / N
    PPV = TP / (TP + FP)
    NPV = TN / (TN + FN)
    FNR = FN / P;
    FDR = FP / (FP + TP)
    ACC = (TP + TN) / (P + N)
    F1 = 2 * (PPV * TPR) / (PPV + TPR)
    print("P={0},N={1},TP={2},TN={3},FN={4},FP={5}".format(P, N, TP, TN, FN, FP))
    print("ACC={0},F1={1}".format(ACC, F1))
    print("##############################################")

