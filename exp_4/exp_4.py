"""Matt's HTM Experiment 4

"""

import exputils
import numpy
import os
import random

os.system("clear")
print "Executing Matt's HTM Experiment 4\n"


#--------------------------------------- setup ----------------------------------
outputImagePrefix = "exp_4_"
outputImageMask = outputImagePrefix + "*.png"
exputils.deleteImages(outputImageMask);
exputils.deleteImages(outputImagePrefix + "*.gif");

inputWidth = 1000
inputHeight = 1000

generateOutputMovie = True

i1 = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
flati1 = i1.flatten()

i2 = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
flati2 = i2.flatten()

def xorInputs(i1, i2):
	length = len(i1)
	outputData = numpy.zeros(shape = length, dtype = "uint8")
	for x in xrange(0, len(i1)):
		if i1[x] != i2[x]:
			outputData[x] = 1
	return outputData

i3 = xorInputs(flati1, flati2)

data = [flati1, flati2, i3]			
#--------------------- main loop  -----------------------
print "starting main loop"
for cycle in xrange(0, len(data)):
	d = data[cycle]
	entropy = exputils.calcEntropy(d)
	print str(cycle) + ": " + exputils.vectorToString(d), "e = " + str(entropy["entropy"]) + " me = " + str(entropy["metricEntropy"])
	unflattenedInput = exputils.unflattenArray(d, inputWidth)
	if generateOutputMovie:
		exputils.writeMatrixImage(unflattenedInput, outputImagePrefix + str(cycle).zfill(5) + ".png")
	
if generateOutputMovie:
	exputils.generateMovie(outputImageMask, outputImagePrefix + "movie.gif", fps = 15)
