#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from PIL import Image
import scipy.misc

xDim = 3300
yDim = 520
y_division_offset = 6
medianConst=-0.005	#-0.07
whiteLineThickness = 0.02
transparentLineThickness=0.07
xpad = 700
ypad = 30
highestConst=medianConst+transparentLineThickness/2
upperConst = medianConst+whiteLineThickness/2
lowerConst = medianConst-whiteLineThickness/2
lowestConst =medianConst-transparentLineThickness/2
topPic = "parkourHelvetica.PNG"
lowPic = "physicsHelvetica.PNG"
def xyFrac(x,y):
	return (x/xDim), y/(yDim-y_division_offset)
def aboveRegion(x,y,const):
	xFrac,yFrac = xyFrac(x,y)
	if (xFrac-yFrac)>const:
		return True
	else:
		return False
def white():
	return ary([255,255,255,255])
def transparent():
	return ary([0,0,0,0])
def picFast(picNum,x,y,xDim,yDim):
	#xDim,yDim = np.shape(picNum)
	if (x in range(xDim)) and (y in range(yDim)):
		pixelValue = ary(picNum[x,y][:3])	#take only the first three values
		pixelValue = ary([255,255,255])-pixelValue
		return np.append(pixelValue,int(np.mean(pixelValue)))
	else:
		return transparent()

#Note: for pictures, the y axis points from top to bottom on ths graphing method.
pixels = ()
f = Image.open(topPic)
pic1 = f.load()
pic1_xDim,pic1_yDim = f.size
f.close()

g = Image.open(lowPic)
pic2 = g.load()
pic2_xDim,pic2_yDim = g.size
g.close()

#Takes too long to use PIL to create the image itself. Instead scipy.misc is used.
img = np.zeros([yDim,xDim,4], dtype = int)
for y in range(yDim):
	print("processing line",str(y+1)+"/"+str(yDim), end="\r")
	for x in range(xDim):
		if  aboveRegion(x,y,highestConst):	#above the top division line
			if x<1000:	#everything to the left of the "P" in Parkour
				img[y][x]= picFast(pic1,x-xpad,y-ypad,pic1_xDim,pic1_yDim)
			else:	#shift everything on the right upwards
				img[y][x]= picFast(pic1,x-xpad,y-ypad+ypad*1,pic1_xDim,pic1_yDim)
		elif not aboveRegion(x,y,lowestConst):	#below the lower division line
			img[y][x]= picFast(pic2,x-xpad,y-ypad,pic2_xDim,pic2_yDim)
		elif (not aboveRegion(x,y,upperConst)) and aboveRegion(x,y,lowerConst):	#between the middle two constants
			img[y][x]= white()
		else:
			img[y][x]= transparent()
opacityMatrix = img[:,:,3]
nonzero = opacityMatrix!=0
nonTwoFiveFive = opacityMatrix!=255
print(np.sum(nonzero*nonTwoFiveFive))

scipy.misc.imshow(img)
scipy.misc.imsave("parkourPhysics_split.png",img)