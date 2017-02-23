from PIL import Image,ImageFilter,ImageEnhance
import os

#define binarzingImage class
class BinarizingImage:
	img = Image.Image()
	threshold = 0

	def loadPicture(self, _filePath, _threshold):
		try:
			#gray image
			filePath = _filePath 
			self.threshold = _threshold
			self.img = Image.open(_filePath).convert("L")
			self.binarizing()
			self.depoint()
			return self.img
		except IOError as err:
			print err

	def binarizing(self):
		#image load matrix
		pixdata = self.img.load()
		w, h = self.img.size
		for y in range(h):
		    for x in range(w):
		        if pixdata[x, y] < self.threshold:
		            pixdata[x, y] = 0
		        else:
		            pixdata[x, y] = 255
	def depoint(self):   #input: gray image
		#self.img.show()
		pixdata = self.img.load()
		w,h = self.img.size

		threshold = 200
		for x in range(0,w):        #remove outline
			pixdata[x,0] = 255
			pixdata[x,h-1] = 255
		for y in range(0,h):
			pixdata[0,y] = 255
			pixdata[w-1,y] = 255

		# filtering lines
		offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (-1, 1), (0, 1), (1, 1)]
		offsets4 = [(-1, 0), (0, -1), (1, 0), (0, 1)]
		for y in range(1, h-1):
	 		for x in range(1, w-1):
	 			if pixdata[x, y] == 0:
		 			count = 0
					for xoffset, yoffset in offsets4:
						xo, yo = x + xoffset, y + yoffset
						if pixdata[xo, yo] == 255:
							count += 1
					if count > 2:
						pixdata[x, y] = 255

		for y in range(1, h-1):
	 		for x in range(1, w-1):
	 			if pixdata[x, y] == 0:
		 			count = 0
					for xoffset, yoffset in offsets:
						xo, yo = x + xoffset, y + yoffset
						if pixdata[xo, yo] == 255:
							count += 1
					if count > 5:
						pixdata[x, y] = 255

		for x in range(w):
			count = 0
			for y in range(h):
				if pixdata[x,y] != 255:
					count += 1
			if count < 2:
				for y in range(h):
					pixdata[x,y] = 255
		#self.img.show()
	    #@Liu
		flags = {}      #indicate point belong to which component
		count = {}      #indicate component's size
		count[1000] = -4    #represent 'white'
		comp = 0        #component number
		label = {}
		for x in range(0,w):        #remove outline
			flags[x,0] = 1000
			flags[x,h-1] = 1000
			count[1000] += 2
		for y in range(0,h):
			flags[0,y] = 1000
			flags[w-1,y] = 1000
			count[1000] += 2
		offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
		# scan component
		for y in range(1, h - 1):
			for x in range(1, w - 1):
				if pixdata[x,y] != 255:
					s = 1000
					l = 1000
					for xoffset, yoffset in offsets:
						xo, yo = x + xoffset, y + yoffset
						s = min(flags[xo, yo], s)
						if flags[xo, yo]<1000 and flags[xo, yo]>s:
							l = flags[xo, yo]
					if s == 1000:
						comp += 1
						flags[x,y] = comp
						count[comp] = 0
					else:
						flags[x,y] = s
						count[flags[x,y]] += 1
						if l != 1000:
							label[l] = s
				else:
					flags[x,y] = 1000
					count[1000] += 1

		# Union equal components from bottom to top
		for y in range(1, h - 1):
			y = h -1 - y
			for x in range(1, w - 1):	
				if flags[x,y] in label:
					count[flags[x,y]] -= 1
					flags[x,y] = label[flags[x,y]]
					count[flags[x,y]] += 1

		# delate small component
		for y in range(1, h - 1):
			for x in range(1, w - 1):
				if(count[flags[x,y]]<10):
					pixdata[x,y] = 255



		#self.img=self.img.filter(ImageFilter.ModeFilter)

	#Equal distance splitting
	def equidistanceSegment(self):
		pixdata = self.img.load()
		w, h = self.img.size
		width = w/4
		newImage = []
		for i in range(4):
			newImage.append( self.img.crop((width*i, 0, width*(i+1),h))) 
		return newImage

#define a class saving the slitted images
class savingImage:
	val = 0

	def saveImage(self, images):
		if images:
			for item in images:
				item.save('splitPhotos/'+ str(self.val) + '.bmp')
				self.val += 1

if __name__ == '__main__':	
	binary = BinarizingImage()
	saveimage = savingImage()

	for i in range(100):
		filePath = 'pictures/' + str(i) + '.jpg'
		img = binary.loadPicture(filePath, 80)
		#img.show()
		imgs = binary.equidistanceSegment()
		saveimage.saveImage(imgs)