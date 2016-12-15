import time
import numpy
import matplotlib.pyplot as pyplot

#  -------------------------- scatter plot style -----------------------------
#def getRandomScatterValues():
#	width = 5
#	height = 5
#	someBitmap = numpy.zeros(shape = (width, height), dtype = "uint8")
#	for x in xrange(0, width):
#		for y in xrange(0, height):
#			someBitmap[x, y] = random.randint(0, 1)
#
#	x = []
#	y = []
#	s = []
#	for xi in xrange(0, width):
#		for yi in xrange(0, height):
#			x.append(xi)
#			y.append(yi)
#			s.append(10 * someBitmap[xi, yi])
#
#	return {"x": x, "y": y, "s": s}
#
#def refreshImage(scatterVals, initialize = False):
#	pyplot.cla()
#	scatterPlot = pyplot.scatter(
#		x = scatterVals["x"],
#		y = scatterVals["y"],
#		s = scatterVals["s"],
#		marker = "s"
#	)
#	if initialize:
#		pyplot.show(block = False)
#	else:
#		pyplot.draw()
#	return scatterPlot
#
## scatter plot updating, 42 seconds
#startTime = time.time()
#refreshImage(scatterVals = getRandomScatterValues(), initialize = True)
#for t in xrange(0, 255):
#	refreshImage(scatterVals = getRandomScatterValues())
#print("--- %s seconds ---" % (time.time() - startTime))

# ----------------------------------- image plot style ----------------------------
#def refreshImage(numpyArray, initialize = False):
#	imgplot = pyplot.imshow(X = numpyArray, interpolation = "none")
#	if initialize:
#		pyplot.show(block = False)
#	else:
#		pyplot.draw()
#	return imgplot
#
# image updating, 132 seconds
#someBitmap = numpy.zeros(shape = (10, 10, 3), dtype = "uint8")
#someBitmap[0][0] = [255, 0, 0]
#someBitmap[4][4] = [255, 255, 255]
#refreshImage(numpyArray = someBitmap, initialize = True)
#startTime = time.time()
#for t in xrange(0, 255):
#	someBitmap[6][6] = [t, t, t]
#	refreshImage(numpyArray = someBitmap)
#print("--- %s seconds ---" % (time.time() - startTime))


# ----------------------------------- 2d histogram test style ----------------------------
#from matplotlib.colors import LogNorm
#from pylab import *
#
#def refreshImage(x, y, initialize = False):
#	pyplot.cla()
#	histogram = pyplot.hist2d(x, y, bins = 10, norm = LogNorm())
#	if initialize:
#		pyplot.show(block = False)
#	else:
#		pyplot.draw()
#	return histogram
#
## image updating, 36 seconds
#startTime = time.time()
#x = randn(10)
#y = randn(10) + 5
#refreshImage(x, y, True)
#for t in xrange(0, 255):
#	x = randn(10)
#	y = randn(10) + 5
#	refreshImage(x, y, False)
#print("--- %s seconds ---" % (time.time() - startTime))
#

# ----------------------------------- matshow test style ----------------------------
# this seems to be the best!
import random as rnd
from matplotlib.pylab import *
from scitools.std import *
import glob, os

def getRandomMatrix():
	width = 1000
	height = 1000
	data = numpy.zeros(shape = (width, height), dtype = "uint8")
	for x in xrange(0, width):
		for y in xrange(0, height):
			data[x, y] = rnd.randint(0, 1)
	return data

def refreshImage(data, initialize = False):
	pyplot.cla()
	ms = matshow(data, fignum = False, cmap = cm.binary)
	if initialize:
		pyplot.show(block = False)
	else:
		pyplot.draw()
	return ms

# clean up old image files
for filename in glob.glob('matshow_*'):
    os.remove(filename)

# image updating, 33 seconds
startTime = time.time()
data = getRandomMatrix()
fig = pyplot.figure()
refreshImage(data, True)
fig.savefig("matshow_000.png")
for t in xrange(1, 10):
	data = getRandomMatrix()
	refreshImage(data, False)
	fig.savefig("matshow_" + str(t).zfill(3) + ".png")
movie("matshow_*.png", encoder = "convert", output_file = "matshow_test.gif", fps = 10)
print("--- %s seconds ---" % (time.time() - startTime))


#---- try Hinton diagram?  matshow? pcolor ----

time.sleep(5)
