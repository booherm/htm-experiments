import BitArray2D
import numpy
import matplotlib.pyplot as pyplot
from matplotlib.pylab import *
#from scitools.std import *
#import glob
#import os

def getBitArray2DFromBitmapFile(filename, width):
	array = numpy.fromfile(file = filename, dtype = "uint8")[62 : ] # stripping header
	bitArray = []
	for byte in array:
		backwardsByte = []
		for bit in xrange(8):
			invertedBit = (byte >> bit) & 1
			finalBit = 0
			if invertedBit == 0:
				finalBit = 1
			backwardsByte.append(finalBit)
			
		for bit in xrange(7, -1, -1):
			bitArray.append(backwardsByte[bit])

	data = BitArray2D.BitArray2D(rows = width, columns = width)
	for row in xrange(0, width):
		for col in xrange(0, width):
			data[(width - 1) - row, col] = bitArray[(width * row) + col]
	#		data[row, col] = bitArray[(width * row) + col]
			
	return data
	
def writeNumpyArrayImage(numpyArray, filename):
	fig = pyplot.figure(figsize = (18, 18), dpi = 80)
	pyplot.cla()
	ms = matshow(numpyArray, fignum = False, cmap = cm.binary)
	fig.savefig(filename)
	pyplot.close()

def writeBitArray2DImage(bitArray, filename):
	# copy BitArray2D to numpy array
	data = numpy.empty(shape = (bitArray.rows, bitArray.columns), dtype = "bool")
	for row in xrange(0, bitArray.rows):
		for col in xrange(0, bitArray.columns):
			data[row, col] = bitArray[BitArray2D.godel(row, col)]
	
	writeNumpyArrayImage(numpyArray = data, filename = filename)
