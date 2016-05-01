import csv
import sys
from sklearn import tree
from sklearn import cross_validation

def prediction(feat,label):
    x_train, x_test, y_train, y_test = cross_validation.train_test_split(feat, label, test_size = 0.25, random_state = 0)
    for depth in range(1,14):
        clf = tree.DecisionTreeClassifier(max_depth = depth)
        clf.fit(x_train,y_train)
        accuracy = clf.score(x_test,y_test)
        print depth,accuracy

def getValues(filename):
    featureIndex = [1,2,3,4,10,15,25,28,29,30,31,32,34]
    baseFeat = []
    label = []
    features = []
    
    with open(filename) as data:
        reader = csv.reader(data,delimiter = ',')
        for row in reader:
            if row[11] > 50:
                temp = []
                for feature in featureIndex:
                    temp.append(float(row[feature]))
                    features.append(temp)
                    baseFeat.append([row[10],row[34]])
                    label.append(float(row[-1]))
    return baseFeat, features,label
if __name__ == '__main__':
    filename = sys.argv[1]
    baseFeat,features, label  = getValues(filename)
    prediction(baseFeat,label)
    prediction(features,label)
    
