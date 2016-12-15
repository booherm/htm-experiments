"""Matt's HTM Experiment 3

"""

import exputils
import numpy
import os
import random

os.system("clear")
print "Executing Matt's HTM Experiment 3\n"


#--------------------------------------- setup ----------------------------------
outputImagePrefix = "exp_3_"
outputImageMask = outputImagePrefix + "*.png"
exputils.deleteImages(outputImageMask);
exputils.deleteImages(outputImagePrefix + "*.gif");

inputWidth = 500
inputHeight = 500

generateOutputMovie = True

input = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
flatInput = input.flatten()
			
#--------------------- main loop  -----------------------
print "starting main loop"
for cycle in xrange(0, 48):
	#print "Flat input: "
	entropy = exputils.calcEntropy(flatInput)
	print str(cycle) + ": " + exputils.vectorToString(flatInput), "e = " + str(entropy["entropy"]) + " me = " + str(entropy["metricEntropy"])
	unflattenedInput = exputils.unflattenArray(flatInput, inputWidth)
	if generateOutputMovie:
		exputils.writeMatrixImage(unflattenedInput, outputImagePrefix + str(cycle).zfill(5) + ".png")

	input = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
	flatInput = input.flatten()
		
if generateOutputMovie:
	exputils.generateMovie(outputImageMask, outputImagePrefix + "movie.gif", fps = 24)
