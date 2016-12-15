"""Matt's HTM Experiments"""

import numpy
import os
from nupic.encoders.category import CategoryEncoder
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.TP import TP

def wait():
	raw_input("Press Enter to continue...")

os.system("clear")
print "Executing Matt's HTM Experiments\n"
print "initializing categories"
inputCategoriesWindowWidth = 3
inputCategoriesRaw = (
	"cat",
	"dog",
	"penguin",
	"potato"
)
categoryEncoder = CategoryEncoder(w = inputCategoriesWindowWidth, categoryList = inputCategoriesRaw, forced = True, verbosity = 0)
inputCategories = {}
for category in inputCategoriesRaw:
	inputCategories[category] = categoryEncoder.encode(category);
	print "   " + (category + ":").ljust(10), inputCategories[category]
print "   " + "UNKNOWN:".ljust(10), categoryEncoder.encode("UNKNOWN");
print "categories initialized\n"

print "initializing spatial pooler"
spatialPoolerInputWidth = (len(inputCategoriesRaw) + 1) * inputCategoriesWindowWidth
spatialPoolerColumnHeight = 8

spatialPooler = SpatialPooler(
	inputDimensions            = spatialPoolerInputWidth,
	columnDimensions           = spatialPoolerColumnHeight,
	potentialRadius            = 15,
	numActiveColumnsPerInhArea = 1,
	globalInhibition           = True,
	synPermActiveInc           = 0.03,
	potentialPct               = 1.0)

print "    spacial pooler initial randomly connected synapses:"
for col in xrange(4):
	currentlyConnected = numpy.zeros(shape = spatialPoolerInputWidth, dtype = "int")
	spatialPooler.getConnectedSynapses(column = col, connectedSynapses = currentlyConnected)
	print "   ", currentlyConnected
print "spatial pooler initialized\n"

spatialPoolerTest = False
if spatialPoolerTest:
	print "iterating some test data"
	for category in ["cat", "dog", "cat", "cat", "dog", "cat", "potato", "potato", "cat", "penguin"]:
		iterationOutput = numpy.zeros(shape = 8, dtype = "int")
		spatialPooler.compute(inputCategories[category], learn = True, activeArray = iterationOutput)
		print (category + ":").ljust(10), iterationOutput
	print "end iterating some test data\n"

print "initializing temporal pooler"
temporalPooler = TP(
	numberOfCols            = 15,
	cellsPerColumn          = 4,
	initialPerm             = 0.5,
	connectedPerm           = 0.5,
	minThreshold            = 10,
	newSynapseCount         = 10,
	permanenceInc           = 0.1,
	permanenceDec           = 0.0,
	activationThreshold     = 3,
	globalDecay             = 0,
	burnIn                  = 1,
	checkSynapseConsistency = False,
	pamLength               = 1 #10
)
print "temporal pooler initialized, temporalPooler.numberOfCols = " + str(temporalPooler.numberOfCols) + "\n"

#print "temporal pooler state:"
#temporalPooler.printStates(printPrevious=False, printLearnState=False)
#wait()

trainTemporalPooler = True
if trainTemporalPooler:
	print "training the temporal pooler"
	for x in xrange(0, 100):
		for category in ["cat", "dog", "penguin", "potato", "cat", "dog", "penguin", "potato"]:
			c = inputCategories[category]
			#print "input: " + category.ljust(10) + " " + str(c)
			temporalPooler.compute(bottomUpInput = c, enableLearn = True, computeInfOutput = True)
			predictedCells = temporalPooler.getPredictedState()
			#print "prediction: " + str(predictedCells)
			#wait()
		temporalPooler.reset()
	#temporalPooler.printCells()
	print "temporal pooler training complete"

def printPredictedCells(cells):
	print "Prediction state:"
	width = len(cells)
	aggregate = list("0" * width)
	for c in xrange(0, len(cells[0])):
		row = ""
		for r in xrange(0, width):
			value = cells[r, c]
			row += str(value);
			if value == 1:
				aggregate[r] = "1"
		print row
	print '-' * width
	print "".join(aggregate)
		
testInferencePrediction = True
if testInferencePrediction:
	print "testing inference prediction"
	temporalPooler.compute(bottomUpInput = inputCategories["potato"], enableLearn = False, computeInfOutput = True)
	printPredictedCells(temporalPooler.getPredictedState())
	print "end testing inference prediction"
