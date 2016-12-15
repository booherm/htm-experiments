"""Matt's HTM Experiment 1

	Input --(2D)--> SP --(1D)--> TP --(1D)--> MAN --(2D) ---|
	  ^_____________________________________________________|

	Manipulation function MAN will be decoding the TP output to 2 coordinates, flipping the bit at that location in the input
"""

import exputils
import numpy
import os
import random
from nupic.research.spatial_pooler import SpatialPooler
#from nupic.research.TP import TP
from nupic.research.TP10X2 import TP10X2 as TP

os.system("clear")
print "Executing Matt's HTM Experiment 1\n"


#--------------------------------------- setup ----------------------------------

outputImagePrefix = "exp_1_"
outputImageMask = outputImagePrefix + "*.png"
exputils.deleteImages(outputImageMask);
exputils.deleteImages(outputImagePrefix + "*.gif");

inputWidth = 50
inputHeight = 50
input = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
generateOutputMovie = True

flatInput = input.flatten()
flatInputLength = len(flatInput)

print "initializing spacial pooler"
spColumnHeight = flatInputLength
spatialPooler = SpatialPooler(
	inputDimensions            = flatInputLength,
	columnDimensions           = spColumnHeight,
	potentialRadius            = 10,
	numActiveColumnsPerInhArea = 1,
	globalInhibition           = True,
	synPermActiveInc           = 0.03,
	potentialPct               = 1.00
)
print "spacial pooler initialization complete\n"

printInitialSynapses = False
if printInitialSynapses:
	print "spacial pooler initial randomly connected synapses:"
	for col in xrange(spColumnHeight):
		currentlyConnected = numpy.zeros(shape = flatInputLength, dtype = "uint8")
		spatialPooler.getConnectedSynapses(column = col, connectedSynapses = currentlyConnected)
		print "   ", currentlyConnected
	print "spatial pooler initialized\n"

genericTest = False
if genericTest:
	print "generic test"
	for i in xrange(0, 10):
		input = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight)
		flatInput = input.flatten()
		#print "flatInput = ", flatInput
		iterationOutput = numpy.zeros(shape = flatInputLength, dtype = "uint8")
		spatialPooler.compute(inputVector = flatInput, learn = True, activeArray = iterationOutput)
		print "Iteration " + str(i) + ":", iterationOutput

print "Initializing temporal pooler"
temporalPooler = TP(
	numberOfCols            = flatInputLength,
	cellsPerColumn          = 104,  # c++ version max = 104
	initialPerm             = 0.5,
	connectedPerm           = 0.5,
	minThreshold            = 10,
	newSynapseCount         = 10,
	permanenceInc           = 0.1,
	permanenceDec           = 0.0,
	activationThreshold     = 1,
	globalDecay             = 0,
	burnIn                  = 1,
	checkSynapseConsistency = False,
	pamLength               = 1
)
print "temporal pooler initiaization complete\n"

## train temporal pooler with all potential spatial pooler outputs
#print "training temporal pooler"
#for x in xrange(0, inputWidth * inputHeight):
#	trainingData = numpy.zeros(shape = flatInputLength, dtype = "int32")
#	trainingData[x] = 1
#	temporalPooler.compute(bottomUpInput = trainingData, enableLearn = True, computeInfOutput = False)
#print "training temporal pooler complete\n"
##temporalPooler.printCells()

# train temporal pooler with desired state
#desiredState = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight).flatten()
#print "training temporal pooler"
#for x in xrange(0, inputWidth * inputHeight * 100):
#	temporalPooler.compute(bottomUpInput = desiredState, enableLearn = True, computeInfOutput = False)
#print "training temporal pooler complete\n"
#temporalPooler.printCells()

# train temporal pooler with random data
print "training temporal pooler"
for x in xrange(0, inputWidth * inputHeight * 100):
	trainingData = exputils.getRandom2dBoolMatrix(inputWidth, inputHeight).flatten()
	temporalPooler.compute(bottomUpInput = trainingData, enableLearn = True, computeInfOutput = False)
print "training temporal pooler complete\n"
#temporalPooler.printCells()


#--------------------- define transform  -----------------------
def applyTransform(base, manipulator):
	# simple bit flip
	for x in range(0, len(manipulator)):
		if manipulator[x] == 1:
			baseValue = base[x]
			if baseValue == 0:
				baseValue = 1
			else:
				baseValue = 0
			base[x] = baseValue

			
			
#--------------------- main loop  -----------------------
print "starting main loop"
for cycle in xrange(0, 200):
	#print "Flat input: "
	entropy = exputils.calcEntropy(flatInput)
	print str(cycle) + ": " + exputils.vectorToString(flatInput), "e = " + str(entropy["entropy"]) + " me = " + str(entropy["metricEntropy"])
	unflattenedInput = exputils.unflattenArray(flatInput, inputWidth)
	if generateOutputMovie:
		exputils.writeMatrixImage(unflattenedInput, outputImagePrefix + str(cycle).zfill(5) + ".png")
	
	spatialPoolerOutput = numpy.zeros(shape = flatInputLength, dtype = "int32")
	spatialPooler.compute(inputVector = flatInput, learn = True, activeArray = spatialPoolerOutput)
	#print "Spatial Pooler output from input: "
	#print exputils.vectorToString(spatialPoolerOutput)
	#print "\n"

	temporalPooler.compute(bottomUpInput = spatialPoolerOutput, enableLearn = True, computeInfOutput = True)
	predictedCells = temporalPooler.getPredictedState()
	#exputils.printPredictedCells(predictedCells)
	predictionVector = exputils.getPredictionVector(predictedCells)
	#print "-" * len(predictionVector)
	#print exputils.vectorToString(predictionVector)
	
	#print "Transformed flat input: "
	#print exputils.vectorToString(flatInput)
	applyTransform(flatInput, predictionVector)
	#print exputils.vectorToString(flatInput)

if generateOutputMovie:
	exputils.generateMovie(outputImageMask, outputImagePrefix + "movie.gif")
