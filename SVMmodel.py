from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib
import csv
import warnings
from sklearn.model_selection import GridSearchCV, cross_val_score

warnings.filterwarnings('ignore')
PKL = 'SVM_PKL.pkl'

#define a SVM model, and use joblib to dump the model as SVM_PKL.pkl
class SVMmodel:
	train_X = np.array([])
	train_y = np.array([])
	#define some parameters of SVC model
	clf = SVC(kernel='rbf', C=1000)

	#load dataset in some format
	def loadData(self, _train_X, _train_y):
		#csv file reader
		ifile = open(_train_X, 'rb')
		reader = csv.reader(ifile)
		train_X = []
		for row in reader:
			line = [ float(item) for item in row ]
			train_X.append(line)
		self.train_X = np.array(train_X)
		ifile.close()
		
		#csv filereader
		ifile = open(_train_y, 'rb')
		reader = csv.reader(ifile)
		train_y = [ row[0] for row in reader ]
		self.train_y = np.array(train_y)
		ifile.close()

	#output function
	def output(self):
		print self.train_y
		print self.train_X
	
	#train SVM on training dataset
	def train(self):
		X = self.train_X
		y = self.train_y
		self.clf.fit(X,y)
		joblib.dump(self.clf, PKL)
		print type(self.clf)

	#define predict function
	def selfTest(self):
		predictvalue = []
		test_X = self.train_X
		for data in test_X:
			predictvalue.append(self.clf.predict(data))

		#calcuate the accuracy of self-testing
		count1 = 0.0
		count2 = 0.0
		for i in range(len(predictvalue)):
			if predictvalue[i] == self.train_y[i]:
				count1 += 1
			else:
				count2 += 1
		print count1/(count1+count2)

	#find the best parameters
	def searchBestParameter(self):
		parameters = {'kernel':['rbf','linear','poly','sigmoid'],'C':[1,100]}
		svr = SVC()
		self.clf = GridSearchCV(svr, parameters)

		X = self.train_X
		y = self.train_y
		
		self.clf.fit(X,y)
		print self.clf.best_params_

	#cross validation
	# def crossValidation(self):
	# 	clf = SVC(kernel='rbf', C=1000)
	# 	X = self.train_X
	# 	y = self.train_y
	# 	scores = cs.cross_val_score(clf, X, y, cv=5)
	# 	print ('accuracy: %0.2f (+/- %0.2f)') % (scores.mean(), scores.std()*2) 


if __name__ == '__main__':
	# main call
	model = SVMmodel()
	model.loadData('traindataX.csv', 'traindatay.csv')
	model.searchBestParameter()
	# model.crossValidation()
	model.train()
	model.selfTest()
	model.output()


