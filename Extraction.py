import numpy as np
import os
import csv
from PIL import Image

def ofile_writer(name, data_writer):
	ofile  = open(name, "wb")
	writer = csv.writer(ofile)
	for each in data_writer:
		writer.writerow(each)
	ofile.close()

#class extrctFeatures, extract pictures to binary image
class extractFeatures:	
	fileNameDic = {}
	dirs = 0

	#extract features
	def getBinaryPixel(self, _filePath):
		try:
			filePath = _filePath 
			img = Image.open(_filePath)
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

		except IOError as err:
			print err

	#Scanning all the files in the dirs
	#saving files' path
	def getFileNames(self, _dirs):
		self.dirs = _dirs
		for folder in os.listdir(self.dirs):
			try:
				newarray = []
				for filename in os.listdir(self.dirs + '/' + folder):
					if filename != '.DS_Store':
						newarray.append(filename)
				self.fileNameDic[folder] = newarray
			except OSError as err:
				print err
		print self.fileNameDic

	#Writing train data
	def writeFile(self):
		ofile_X = open('traindataX.csv','w')
		ofile_y = open('traindatay.csv','w')
		ofile_Z = open('traindataZ.csv','w')

		writer_X = csv.writer(ofile_X, delimiter=',')
		writer_y = csv.writer(ofile_y)
		writer_Z = csv.writer(ofile_Z, delimiter=',')
		
		for key in self.fileNameDic:
			if key != '.\n':
				for filename in self.fileNameDic[key]:
					binaryPixel = self.getBinaryPixel(self.dirs+'/'+key+'/'+filename)	
					writeData = [item for item in binaryPixel]
					writer_X.writerow(writeData)
					writer_y.writerow(key)
					
					writeData = [key]
					for item in binaryPixel:
						writeData.append(item)
					writer_Z.writerow(writeData)

		ofile_X.close()
		ofile_y.close()
		ofile_Z.close()

#main call
if __name__ == '__main__':
	extractClass = extractFeatures()
	filePath = '/Users/guangyang/Desktop/code/trainingDataset'
	extractClass.getFileNames(filePath)
	extractClass.writeFile()
	
	# the following progarm is used to show some pictures for the report
	# binaryPixel = extractClass.getBinaryPixel('/Users/guangyang/Desktop/code/splitPhotos/0.bmp')
	# print binaryPixel[0:18]
	# shows = [ binaryPixel[i*18:i*18+18] for i in range(0,20) ]
	# print 'the image is like:'
	# print shows
	# print 'the extraction features are like:'
	# print binaryPixel
	# ofile_writer('9.csv', shows)

