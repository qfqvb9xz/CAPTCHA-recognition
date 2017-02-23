import os

path = 'splitPhotos/'
newpath = 'trainingDataset/'

for i in range(4000,10000):
	with open(path+str(i)+'.txt') as fp:
		for j in fp:
			print j
			try:
				os.mkdir(newpath+j)
				os.rename(path+str(i)+'.bmp', newpath+j+'/'+str(i)+'.bmp')
			except OSError:
				os.rename(path+str(i)+'.bmp', newpath+j+'/'+str(i)+'.bmp')
			break
		fp.close()