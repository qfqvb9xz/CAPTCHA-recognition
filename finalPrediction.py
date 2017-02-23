import numpy as np
from PIL import Image
from sklearn.svm import SVC
from sklearn import grid_search
from sklearn import cross_validation as cs
from sklearn.externals import joblib
from binary import BinarizingImage
import warnings

warnings.filterwarnings('ignore')

#class extrctFeatures, extract pictures to binary image
class extractFeatures:	
	#extract features
	def getBinaryPixel(self, img):
		img = np.array(img)
		row, col = img.shape
		for x in range(row):
			for y in range(col):
				if img[x,y] == 0:
					img[x,y] = 1
				else:
					img[x,y] = 0
		binaryPixel = np.ravel(img)
		return binaryPixel 	

#class predictionModel to varify a new image
class predictionModel:
	test_X = np.array([])

	def loaddata(self, filePath):
		binary = BinarizingImage()
		img = binary.loadPicture(filePath, 80)

		imgs = binary.equidistanceSegment()		
		extract = extractFeatures()
		testdata = []
		for item in imgs:
			line = extract.getBinaryPixel(item).tolist()
			testdata.append(line)
		self.test_X = np.array(testdata)

	def SVMpredict(self):
		clf = joblib.load('SVM_PKL.pkl')
		predictvalue = []
		for data in self.test_X:
			predictvalue.append(clf.predict(data)[0])
		print predictvalue

#####################
####  main call  ####
#####################
if __name__ == '__main__':	
	filePath = 'imgcode.jpg'
	img = Image.open(filePath)
	img.show()
	model = predictionModel()
	model.loaddata(filePath)
	model.SVMpredict()



