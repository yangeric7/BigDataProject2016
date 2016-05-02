import scipy
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

#name, mvptfidf, champshiptfidf, awardtfidf, timetfidf, yr, team, gameswon, pos, age, gp, gs, min, fg, fga, fg%, 3p,
#3pa, 3p%, 2p, 2pa, 2p%, efg%, ft, fta, ft%, orb, drb, trb, a, stl, blk, tov, pf, pts, mvp label
def load_data():
    f = open('CombinedData.csv', 'r')
    lines = f.readlines()
    f.close()
    data = []
    for line in lines:
        line = line.strip()
        data.append(line.split(','))
    return data
        
#returns the features of the data specified in features
#features should be in range(0, len(data))
#features should be numbers, or strings that can be converted to numbers
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

#returns a list of the output label for the data, in this case the MVP label, which is feature 35	
def createoutput(data):
	output = []
	for i in range(0, len(data)):
		output.append(float(data[i][35]))
		#output.append(float(data[i][31]))
	return output
		
#if sample_size equals number of samples in input, execution proceeds normally
#data is split into testing and training sets, and accuracy and auc are calculated
#if sample_size != number of samples, create new input to be passed into train_test_split
#using random number generator until sample of with sample_size samples has been created
#if sample_size != len(input) assume sample_size is less than len(input)
def test_classifier(clf, input, output, sample_size):
	new_input = input
	new_output = output
	if sample_size != len(input):
		numbers_used = []
		new_input = []
		new_output = []
		while len(new_input) != sample_size:
			rand = random.randint(0, len(output) - 1)
			if rand not in numbers_used:
				new_input.append(input[rand])
				new_output.append(output[rand])
				numbers_used.append(rand)
	X_train, X_test, Y_train, Y_test = train_test_split(new_input, new_output, test_size = 0.25, random_state = 0)
	clf.fit(X_train, Y_train)
	prediction = clf.predict(X_test)
	accuracy = clf.score(X_test, Y_test)
	auc = roc_auc_score(Y_test, prediction)
	return [accuracy, auc]
		
def main():
    data = load_data()
    baseline_features = [10, 34] #games played and points
    boxscore_features = [10, 15, 25, 28, 29, 30, 31, 32, 34] #games played, fg%, total reb, assists, steals, blocks, turnovers, pts
    combined_features = [1, 2, 3, 4, 10, 15, 25, 28, 29, 30, 31, 32, 34] #combine boxscore features with tfidf features
    #baseline_features = [6, 30]
    #boxscore_features = [6, 11, 21, 24, 25, 26, 27, 28, 30]
    baseline_input = createinput(data, baseline_features)
    boxscore_input = createinput(data, boxscore_features)
    combined_input = createinput(data, combined_features)
    output = createoutput(data)
    
    clf = GaussianNB()
    sample_sizes = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, len(output)]
    baseline_auc = []
    baseline_accuracy = []
    boxscore_auc = []
    boxscore_accuracy = []
    combined_auc = []
    combined_accuracy = []
    for sample_size in sample_sizes:
    	baseline_results = test_classifier(clf, baseline_input, output, sample_size)
    	boxscore_results = test_classifier(clf, boxscore_input, output, sample_size)
    	combined_results = test_classifier(clf, combined_input, output, sample_size)
    	baseline_accuracy.append(baseline_results[0])
    	baseline_auc.append(baseline_results[1])
    	boxscore_accuracy.append(boxscore_results[0])
    	boxscore_auc.append(boxscore_results[1])
    	combined_accuracy.append(combined_results[0])
    	combined_auc.append(combined_results[1])
    
    #plot results for GaussianNB accuracy, comparing baseline vs boxscore vs combined
    plt.figure(5)
    plt.plot(sample_sizes, baseline_accuracy, 'o-', color = 'r', label = 'Baseline')
    plt.plot(sample_sizes, boxscore_accuracy, 'o-', color = 'b', label = 'Boxscore')
    plt.plot(sample_sizes, combined_accuracy, 'o-', color = 'y', label = 'Combined')
    plt.suptitle('MVP Prediction: Accuracy of Gaussian Naive Bayes', fontsize = 24)
    plt.xlabel('Number of samples used in training set')
    plt.ylabel('Accuracy')
    plt.legend()
  

    plt.figure(6)
    plt.plot(sample_sizes, baseline_auc, 'o-', color = 'r', label = 'Baseline')
    plt.plot(sample_sizes, boxscore_auc, 'o-', color = 'b', label = 'Boxscore')
    plt.plot(sample_sizes, combined_auc, 'o-', color = 'y', label = 'Combined')
    plt.suptitle('MVP Prediction: Area Under Curve of Gaussian Naive Bayes', fontsize = 24)
    plt.xlabel('Number of samples used in training set')
    plt.ylabel('Area under curver')
    plt.legend()
	#plt.show()
	
    
    kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    baseline_auc = []
    baseline_accuracy = []
    boxscore_auc = []
    boxscore_accuracy = []
    combined_auc = []
    combined_accuracy = []
    for my_kernel in kernels:
    	clf = svm.SVC(kernel = my_kernel)
    	baseline_results = test_classifier(clf, preprocessing.StandardScaler().fit_transform(baseline_input), output, len(baseline_input))
    	boxscore_results = test_classifier(clf, preprocessing.StandardScaler().fit_transform(boxscore_input), output, len(baseline_input))
    	combined_results = test_classifier(clf, preprocessing.StandardScaler().fit_transform(combined_input), output, sample_size)
    	baseline_accuracy.append(baseline_results[0])
    	baseline_auc.append(baseline_results[1])
    	boxscore_accuracy.append(boxscore_results[0])
    	boxscore_auc.append(boxscore_results[1])
    	combined_accuracy.append(combined_results[0])
    	combined_auc.append(combined_results[1])
    
    print combined_accuracy
    print combined_auc
    
    N = len(kernels)
    ind = np.arange(N)
    width = 0.30
    
    fig1, ax1 = plt.subplots()
    rects1 = ax1.bar(ind, baseline_auc, width, color = 'r')
    
    rects2= ax1.bar(ind + width, boxscore_auc, width, color = 'b')
    rects3= ax1.bar(ind + 2 * width, combined_auc, width, color = 'y')
    ax1.set_ylabel('Area Under Curve')
    ax1.set_title('Area Under Curve Comparison for Various SVM Kernels')
    ax1.set_xticks(ind + width)
    ax1.set_xticklabels(kernels)
    ax1.legend((rects1[0], rects2[0], rects3[0]), ('Baseline', 'Boxscore', 'Combined'))
    
    fig2, ax2 = plt.subplots()
    rects4 = ax2.bar(ind, baseline_accuracy, width, color = 'r')
    rects5 = ax2.bar(ind + width, boxscore_accuracy, width, color = 'b')
    rects6 = ax2.bar(ind + 2*width, combined_accuracy, width, color = 'y')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Accuracy Comparision for Various SVM Kernels')
    ax2.set_xticks(ind + width)
    ax2.set_xticklabels(kernels)
    ax2.legend((rects4[0], rects5[0], rects6[0]), ('Baseline', 'Boxscore', 'Combined'))
    
    plt.show()
    
    
if __name__ == '__main__':
    main()