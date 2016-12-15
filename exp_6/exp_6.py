"""Matt's HTM experiment 6

Goal:	Symbol activation
	1) run distinct pictures p1...pn through the symbol generator, storing both the pictures and symbols (parallel arrays)
	2) pick out one of the p1..pn pictures loaded.  Call this testPicture
	3) make some subtle alteration to testPicture and run it through the symbol generator.  Call this output testSymbolPrime
	4) compare testSymbolPrime to all symbols initially stored.  Track the minimum difference resulting from XOR

	It will have a 1 in pn chance of matching by random chance.  Increase pn to rule it out.
"""

from symbol_generator_3 import *
import exputils
import numpy
import os
import random

experimentId = "6_0"

os.system("clear")
print "Executing Matt's general intelligence experiment " + experimentId + "\n"


#--------------------------------------- image / movie output setup  ----------------------------------
outputImagePrefix = "exp_" + experimentId + "_"
outputImageMask = outputImagePrefix + "*.png"
exputils.deleteImages(outputImageMask);
exputils.deleteImages(outputImagePrefix + "*.gif");

#---------------------------------------------- the test -----------------------------------------------
inputWidth = 64
inputData = exputils.getRandomBooleanMatrix(inputWidth)
previousEntropy = -1
mainSymbolGenerator = SymbolGenerator(matrix = inputData, outputImageFilenamePrefix = outputImagePrefix)
mainSymbolGenerator.process()

#for cycle in xrange(0, 20):
#
#	currentEntropy = exputils.calcEntropy(inputData.flatten())
#	if previousEntropy != currentEntropy:
#		previousEntropy = currentEntropy
#		print "iteration", cycle, "initial entropy", currentEntropy
#		mainSymbolGenerator = SymbolGenerator()
#		mainSymbolGenerator.process(matrix = inputData)
#		print "iteration", cycle, "final entropy", mainSymbolGenerator.finalEntropy
#		exputils.writeMatrixImage(mainSymbolGenerator.matrix, outputImagePrefix + str(cycle).zfill(5) + ".png")
#		inputData = mainSymbolGenerator.matrix


# generate pictures 0 through pictureCount - 1 storing off generated picture and derived symbols
#pictureCount = 200
#pictures = []
#symbols = []
#for pictureIndex in xrange(0, pictureCount):
#	print "generating picture", pictureIndex
#	pictureData = exputils.getRandom2dBoolMatrix(inputWidth, inputWidth)
#	initialEntropy = exputils.calcEntropy(pictureData.flatten())["entropy"]
#	pictures.append(pictureData)
#	exputils.writeMatrixImage(pictureData, outputImagePrefix + "_input_picture_" + str(pictureIndex).zfill(5) + "_" + str(x).zfill(5) + ".png")
#	print "generating picture", pictureIndex, " complete, initial entropy =", initialEntropy
#	
#	print "generating symbol for picture", pictureIndex
#	symbolGenerator = SymbolGenerator()
#	symbolGenerator.process(matrix = pictureData)
#	symbols.append(symbolGenerator.matrix)
#	exputils.writeMatrixImage(symbolGenerator.matrix, outputImagePrefix + "_output_symbol_" + str(pictureIndex).zfill(5) + "_" + str(x).zfill(5) + ".png")
#	print "generating symbol for picture", pictureIndex, " complete, final entropy =", symbolGenerator.finalEntropy
#
#

#def getSymbolDifference(leftMatrix, rightMatrix):
#	# XOR the two together, the output 1 bits are the difference
#	differenceMatrix = symbol_generator.xorMatrices(leftMatrix, rightMatrix)
#	return numpy.count_nonzero(differenceMatrix)
#
#sgtestpic = exputils.getRandom2dBoolMatrix(inputWidth, inputWidth)
#sg = SymbolGenerator()
#sg.process(matrix = sgtestpic)

# Take some arbitrary picture and alter it a little.  THIS NEEDS LIMIT TESTING AND PROOF:
# Translation, rotation, scaling, shear, inverting, flipping all bits, noise, distortion, and ultimately different contexts
# ex., picture of face, picture of face wearing sunglasses
#testPictureIndex = 69
#print "getting a copy and modifying picture", testPictureIndex
#testPictureData = pictures[testPictureIndex][:]  # making a copy
#exputils.writeMatrixImage(testPictureData, outputImagePrefix + "_input_test_picture_orignial.png")
#
# For this test, it will be a simple translation, shift all the bits down 2 slots and to the right 4 slots, and wrapping around.
#testPictureDataModified = numpy.roll(testPictureData, shift = 4, axis = 0)
#testPictureDataModified = numpy.roll(testPictureDataModified, shift = 2, axis = 1)
#exputils.writeMatrixImage(testPictureData, outputImagePrefix + "_input_test_picture_modified.png")
#
## get the symbol for testPictureDataModified
#print "generating testPictureDataModified symbol, initial entropy =", exputils.calcEntropy(testPictureDataModified.flatten())
#sg = SymbolGenerator()
#sg.process(matrix = testPictureDataModified)
#testSymbolPrime = sg.matrix
#exputils.writeMatrixImage(testSymbolPrime, outputImagePrefix + "_test_symbol_prime_" + str(pictureIndex).zfill(5) + ".png")
#print "testSymbolPrime symbol generation complete, final entropy:", sg.finalEntropy
#
#print "looking for closest match..."
## check for closest match
#minSymbolDiff = None
#minDiffSymbolIndex = 9999
#for symbolIndex in xrange(0, symbols.length)
#	symbolDiff = getSymbolDifference(symbols[symbolIndex], testSymbolPrime)
#	if minSymbolDiff is None or symbolDiff < minSymbolDiff:
#		minSymbolDiff = symbolDiff
#		minDiffSymbolIndex = symbolIndex
#	print "difference between symbol", symbolIndex, " and testSymbolPrime is", symbolDiff, " bits"
#
## hopefully this value is the original testPictureIndex value........
#print "the base picture symbol with the least amount of bit difference is:", minDiffSymbolIndex, ", difference of", minSymbolDiff, " bits"
#
#print "test complete"