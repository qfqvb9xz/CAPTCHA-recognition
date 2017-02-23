import csv
import numpy as np
from PIL import Image
from binary import BinarizingImage
import os

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

#class kmeansmodel using to predict
class kmeansModel:
	train_X = np.array([])
	train_y = np.array([])
	test_X = np.array([])
	
	#load training dataset
	def loadTrainData(self, _train_X, _train_y):		
		ifile = open(_train_X, 'rb')
		reader = csv.reader(ifile)
		train_X = []
		for row in reader:
			line = [ float(item) for item in row ]
			train_X.append(line)
		self.train_X = np.array(train_X)
		ifile.close()
		
		ifile = open(_train_y, 'rb')
		reader = csv.reader(ifile)
		train_y = [ row[0] for row in reader ]
		self.train_y = np.array(train_y)
		ifile.close()

	#load testing image
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

	#kmeans prediction
	def Kmeanspredict(self):
		row1, col1 = self.test_X.shape
		row2, col2 = self.train_X.shape
		labels = []
		for i in range(row1):
			array1 = self.test_X[i]
			distance = 100
			label = 0
			#calculate the minimum distance between the image and training dataset
			for j in range(row2):
				array2 = self.train_X[j]
				temp = np.subtract(array1, array2)
				new_distance = np.dot(temp, temp) ** 0.5
				if new_distance <= distance:
					distance = new_distance
					label = self.train_y[j]
			labels.append(label)
		print labels[0] + labels[1] + labels[2] + labels[3] 
		return labels[0] + labels[1] + labels[2] + labels[3] 

#######################
###### Main Call ######
#######################
if __name__ == '__main__':
	filePath = 'imgcode.jpg'
	img = Image.open(filePath)
	img.show()
	model = kmeansModel()
	model.loaddata(filePath)
	model.loadTrainData('traindataX.csv', 'traindatay.csv')
	model.Kmeanspredict()

	folderPath = 'testpictures_k/'
	
	#classification test
	# for i in range(0,200):
	# 	filePath = folderPath + str(i) + '.jpg'
	# 	img = Image.open(filePath)
	# 	model.loaddata(filePath)
	# 	newname = model.Kmeanspredict()
	# 	os.rename(filePath, folderPath + newname +'.jpg')


	
