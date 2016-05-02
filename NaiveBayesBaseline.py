import scipy
import numpy
import random
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import train_test_split

#name, mvptfidf, champshiptfidf, awardtfidf, timetfidf, yr, team, gameswon, pos, age, gp, gs, min, fg, fga, fg%, 3p,
#3pa, 3p%, 2p, 2pa, 2p%, efg%, ft, fta, ft%, orb, drb, trb, a, stl, blk, tov, pf, pts, mvp label
def load_data():
    f = open('labeljoinstatstfidf.csv', 'r')
    lines = f.readlines()
    f.close()

    data = []
    for line in lines:
        line = line.strip()
        data.append(line.split(','))
    print len(data)
    return data;

#just want points and games played for baseline
#want MVPtfidf, champtfidf, awardtfidf, timetfidf, games won, gp, fg%, trb, a, stl, blk, tov, pts for features
def create_input(data):
    baseline = scipy.zeros((len(data), 2))
    features = []
    features_index = [1, 2, 3, 4, 7, 10, 15, 28, 29, 30, 31, 32, 34]
    for i in range(0, len(data)):
        baseline[i, 0] = data[i][34]
        baseline[i, 1] = data[i][10]
        dataset = []
        for x in features_index:
            dataset.append(data[i][x])
        features.append(dataset)
    return baseline, features

#get MVP label from end of data
def create_output(data):
    Y = scipy.zeros((len(data), 1))
    for i in range(0, len(data)):
        Y[i,0] = data[i][35]
    return Y;

#pass in type of classifier, training data, training labels, size of training set to be used
def test_classifier(clf, X, Y, size):
    numbers_used = []
    new_X = []
    new_Y = []
    results = []
    while len(new_X) != size:
        rand = random.randint(0, len(X) - 1)
        if rand not in numbers_used:
            dataset = []
            for i in range(0,len(X[0])):
                dataset.append(float(X[rand][i]))
            new_X.append(dataset)
            new_Y.append(float(Y[rand][0]))
            numbers_used.append(rand)
    X_train, X_test, Y_train, Y_test = train_test_split(new_X, new_Y, test_size = .25, random_state=0)
    clf.fit(X_train, Y_train)
    prediction = clf.predict(X_test)
    accuracy = clf.score(X_test, Y_test)
    auc = roc_auc_score(Y_test, prediction)
    results.append(accuracy)
    results.append(auc)
    return results

def compare_features(X, Y, clf):
    results = []
    i = 1000
    while i < len(X):
        aucandaccuracy = test_classifier(clf, X, Y, i)
        aucandaccuracy.insert(0,i)
        results.append(aucandaccuracy)
        i = i + 500
    totaltestsetresults = test_classifier(clf, X, Y, len(X))
    totaltestsetresults.insert(0, len(X))
    results.append(totaltestsetresults)
    return results
    


def  main():
    data = load_data();
    baseline_X, features_X = create_input(data);
    Y = create_output(data);
    clf = GaussianNB()
    baseline_results = compare_features(baseline_X, Y, clf)
    feature_results = compare_features(features_X, Y, clf)
    sizes = []
    for i in range(0, len(feature_results)):
        sizes.append(feature_results[i][0])

    baseline_accuracy = []
    features_accuracy = []
    for i in range(0, len(feature_results)):
        baseline_accuracy.append(baseline_results[i][1])
        features_accuracy.append(feature_results[i][1])

    baseline_auc = []
    features_auc = []
    for i in range(0, len(feature_results)):
        baseline_auc.append(baseline_results[i][2])
        features_auc.append(feature_results[i][2])
    plt.figure(1)
    plt.plot(sizes, baseline_accuracy, 'o-', color = 'r', label = 'Baseline')
    plt.plot(sizes, features_accuracy, 'o-', color = 'b', label = 'Actual')
    plt.suptitle('MVP Prediction: Accuracy of Gaussian Naive Bayes', fontsize = 24)
    plt.xlabel('Number of samples used in training set')
    plt.ylabel('Accuracy')
    plt.legend()


if __name__ == '__main__':
    main()
