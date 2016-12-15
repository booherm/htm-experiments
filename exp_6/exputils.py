import numpy
import random as rnd
import matplotlib.pyplot as pyplot
import math
from matplotlib.pylab import *
from scitools.std import *
import glob
import os

def getRandomBooleanMatrix(width):
	data = numpy.empty(shape = (width, width), dtype = "bool")
	for x in xrange(0, width):
		for y in xrange(0, width):
			data[x, y] = bool(rnd.getrandbits(1))
	return data
	
def getPredictionVector(predictionCells):
	width = len(predictionCells)
	aggregate = numpy.zeros(shape = width, dtype = "int32")
	for c in xrange(0, len(predictionCells[0])):
		for r in xrange(0, width):
			value = predictionCells[r, c]
			if value == 1:
				aggregate[r] = "1"
	return aggregate

def printPredictedCells(predictionCells):
	print "Prediction state:"
	width = len(predictionCells)
	for c in xrange(0, len(predictionCells[0])):
		row = ""
		for r in xrange(0, width):
			value = predictionCells[r, c]
			row += str(value);
		print row

def vectorToString(vector):
	return numpy.array_str(vector).translate(None, "[] \n")

def unflattenArray(vector, width):
	flatLength = len(vector)
	height = flatLength / width
	output = numpy.zeros(shape = (width, height), dtype = "int32")
	for row in xrange(0, height):
		for col in xrange(0, width):
			output[row, col] = vector[(row * width) + col]
	return output
	
def writeMatrixImage(matrix, filename):
	fig = pyplot.figure(figsize = (18, 18), dpi = 80)
	pyplot.cla()
	ms = matshow(matrix, fignum = False, cmap = cm.binary)
	fig.savefig(filename)
	pyplot.close()
	
def deleteImages(pattern):
	for filename in glob.glob(pattern):
		os.remove(filename)

def generateMovie(pngFilenamePattern, outputFilename, fps):
	movie(pngFilenamePattern, encoder = "convert", output_file = outputFilename, fps = fps)

def calcEntropy(vector):
	length = len(vector)
	zeros = numpy.count_nonzero(vector)
	ones = length - zeros
	pctZeros = float(zeros) / length
	pctOnes = float(ones) / length
	if pctZeros == 1 or pctOnes == 1:
		entropy = 0
	else:
		entropy = -((math.log(pctZeros, 2) * pctZeros) + (math.log(pctOnes, 2) * pctOnes))
	return {"entropy": entropy, "metricEntropy": (entropy / length)}
