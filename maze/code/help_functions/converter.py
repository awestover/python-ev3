# converts white to transparent backgruond
from PIL import Image
import os

def imgTransparent(imgPath):

	img = Image.open(imgPath)
	img = img.convert("RGBA")
	datas = img.getdata()

	newData = []
	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255:
			newData.append((255, 255, 255, 0))
		else:
			newData.append(item)

	img.putdata(newData)

	img.save("batch\{}".format(imgPath), "PNG")

# for i in range(1, 7):
# 	imgTransparent("die{}.png".format(i))
os.mkdir("batch")
imgTransparent("robot.png")
