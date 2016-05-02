






import scipy
import numpy
import random
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import train_test_split

def load_2016data():
    f = open('2016combinedtfidfplayerdata.csv', 'r')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
        line = line.strip()
        data.append(line.split(','))
    return data

def load_data():
    f = open('CombinedData.csv', 'r')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
        line = line.strip()
        data.append(line.split(','))
    return data
    
def createinput(data, features):
	input = []
	for i in range(0, len(data)):
		my_data = []
		for feature in features:
			if data[i][feature] == '':
			    data[i][feature] = -1
			my_data.append(float(data[i][feature]))
		input.append(my_data)
	return input
	
def createoutput(data):
	output = []
	for i in range(0, len(data)):
		output.append(float(data[i][35]))
		#output.append(float(data[i][31]))
	return output
	
def test_classifier(clf, input, output, data_to_predict_on):
	X_train, X_test, Y_train, Y_test = train_test_split(input, output, test_size = 0.25, random_state = 0)
	clf.fit(X_train, Y_train)
	prediction = clf.predict(data_to_predict_on)
	return prediction
		


def main():
    my2016data = load_2016data()
    combined_data = load_data()
    combined_features = [1, 2, 3, 4, 10, 15, 25, 28, 29, 30, 31, 32, 34]
    combined_input = createinput(combined_data, combined_features)
    my2016_input = createinput(my2016data, combined_features)
    output = createoutput(combined_data)
    clf = GaussianNB()
    results = test_classifier(clf, combined_input, output, my2016_input)
    candidates = []
    for i in range(0, len(my2016data)):
    	if results[i] == 1:
    		candidates.append(my2016data[i][0])
    
    print candidates
    return
    
if __name__ == '__main__':
    main()
    
    