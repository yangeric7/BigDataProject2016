import csv
import sys
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

def prediction(feat,label):
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(feat, label, test_size = 0.25, random_state = 0)
    num_leaves = []
    accuracy_score = []
    auc_score = []
    for depth in range(1,10):
        clf = RandomForestClassifier(n_estimators = 10, max_depth = depth)
        clf.fit(x_train,y_train)
        predictions = clf.predict(x_test)
        accuracy = clf.score(x_test,y_test)
        auc = metrics.roc_auc_score(y_test,predictions)
        num_leaves.append(depth)
        accuracy_score.append(accuracy)
        auc_score.append(auc)

    return num_leaves,accuracy_score,auc_score

def getValues(filename, featureIndex):
    baseFeat = []
    label = []
    features = []
    
    with open(filename) as data:
        reader = csv.reader(data,delimiter = ',')
        for row in reader:
            temp = []
            
            for feature in featureIndex:
                temp.append(float(row[feature]))
            features.append(temp)
            baseFeat.append([float(row[10]),float(row[34])])
            label.append(float(row[-1]))
                
    return baseFeat, features,label

if __name__ == '__main__':
    filename = sys.argv[1]
    featureWiki = [1,2,3,4]
    featureCombined = [1,2,3,4,10,15,25,28,29,30,31,32,34]

    baseFeat,features, label  = getValues(filename, featureWiki)
    baseDepth, baseAcc, baseAUC = prediction(baseFeat,label)
    depth, acc, auc = prediction(features,label)

    baseComb, featComb, labelComb = getValues(filename, featureCombined)
    baseCombDepth, baseCombAcc, baseCombAUC = prediction(baseComb, label)
    CombDepth, CombAcc, CombAUC = prediction(featComb,label)
    
    plt.figure(1)
    plt.plot(baseDepth,baseAcc, 'o-', color = 'r',label = 'Baseline')
    plt.plot(depth,acc, 'o-', color = 'b' ,label = 'Actual')
    plt.suptitle('MVP Prediction: Accuracy of Random Forest', fontsize = 24)
    plt.xlabel('Depth of Random Forest')
    plt.ylabel('Accuracy')
    plt.legend(loc = 'upper left')

    plt.figure(2)
    plt.plot(baseDepth, baseAUC, 'o-', color = 'r', label = 'Baseline')
    plt.plot(depth, auc, 'o-', color = 'b', label = 'Wiki Only')
    plt.plot(CombDepth, CombAUC, 'o-', color = 'g', label = 'Combined')
    plt.suptitle('MVP Prediction: AUC of Random Forest', fontsize = 24)
    plt.xlabel('Depth of Random Forest')
    plt.ylabel('Area Under Curve')
    plt.legend(loc = 'upper left')
    plt.show()