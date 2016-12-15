"""Matt's HTM Experiment 5

"""

import exputils
import numpy
import os
import random

experimentId = 5.1

os.system("clear")
print "Executing Matt's HTM Experiment " + str(experimentId) + "\n"


# TODO
# - no need to copy the sub matrices around, just manipulate one master matrix
# - log status and states to database for analysis, plain text print out is hard to read
# - parallelization
# - change datatype to bool in matrices
# - use numpy xor function
# - pass unflattened matrix to entropy calc
# - add in metric entropy everywhere
# - determine impact of xor of self in sub matrix xor'ing
# - hardcoded assumptions of square matrix
# - add main loop iteration term when entropy stabalizes
# - try triang
# - in case of tie entropy, the algorithm is taking the first min encountered, introducing some bias.
# - 	Change to sort, tie break on:
# -     1) if the matrices are the same, look at matrix layout.  Use matrix values to determine winner
# -     or 2) random - less preferred as we can give the algorithm more choice

#--------------------------------------- image / movie output setup  ----------------------------------
outputImagePrefix = "exp_" + str(experimentId) + "_"
outputImageMask = outputImagePrefix + "*.png"
exputils.deleteImages(outputImageMask);
exputils.deleteImages(outputImagePrefix + "*.gif");
generateOutputMovie = True

#------ mechanism to uniquely identify all matrices
globalIdCounter = -1
def getGlobalId():
	global globalIdCounter
	globalIdCounter += 1
	return globalIdCounter

#------ simple xor of 2 matrices
def xorMatrices(leftMatrix, rightMatrix):
	length = len(leftMatrix)
	outputData = numpy.zeros(shape = (length, length), dtype = "uint8")
	for x in xrange(0, length):
		for y in xrange(0, length):
			if leftMatrix[x, y] != rightMatrix[x, y]:
				outputData[x, y] = 1

	return outputData

class MatrixAnalysis:
	level = None
	initialEntropy = None
	finalEntropy = None
	matrix = None
	matrixWidth = None
	subMatrixAnalyses = None
	globalId = None
	
	def process(self, matrix, level = 0):
		self.level = level
		self.subMatrixAnalyses = []
		self.matrix = matrix
		self.matrixWidth = len(matrix)

		self.globalId = getGlobalId()
		self.initialEntropy = exputils.calcEntropy(self.matrix.flatten())["entropy"]
		
		#print ("    " * level), "processing globalId", self.globalId
		
		if self.matrixWidth > 1:   # we can further descend
		
			winnerMatrixAttributes = None
			for subMatrix in getSubMatrices(self.matrix):
			
				# this could be done in parallel while this parent process blocks until its sub matrices are done
				subMatrixAnalysis = MatrixAnalysis()
				result = subMatrixAnalysis.process(matrix = subMatrix, level = level + 1)
				self.subMatrixAnalyses.append(result)
				
				if winnerMatrixAttributes is None or result.initialEntropy < winnerMatrixAttributes["initialEntropy"]:
					winnerMatrixAttributes = {
						"globalId":       result.globalId,
						"matrix":         result.matrix,
						"initialEntropy": result.initialEntropy
					}

			if winnerMatrixAttributes is None:
				winner = self.subMatrixAnalyses[0]
				winnerMatrixAttributes = {
					"globalId":       result.globalId,
					"matrix":         result.matrix,
					"initialEntropy": result.initialEntropy
				}
			
			#print "determined level", level, winnerMatrixAttributes["globalId"], " entropy:", winnerMatrixAttributes["entropy"]
			# xor winner with all peers, not self
			for subMatrixAnalysis in self.subMatrixAnalyses:
			#	#print ("    " * level), "    applying xor to ", subMatrixAnalysis.globalId
				#if subMatrixAnalysis.globalId != winnerMatrixAttributes["globalId"]:
				subMatrixAnalysis.matrix = xorMatrices(winnerMatrixAttributes["matrix"], subMatrixAnalysis.matrix)
				subMatrixAnalysis.finalEntropy = exputils.calcEntropy(subMatrixAnalysis.matrix.flatten())["entropy"]
			
			# bundle matrices and replace own matrix
			newMatrices = []
			for subMatrixAnalysis in self.subMatrixAnalyses:
				newMatrices.append(subMatrixAnalysis.matrix)
			if len(newMatrices) != 0:
				self.matrix = bundleMatrices(newMatrices)
				self.finalEntropy = exputils.calcEntropy(self.matrix.flatten())["entropy"]
			else:
				self.finalEntropy = self.initialEntropy
			
		return self
	
	def printMatrixAnalysis(self, nestLevel = 0):
		print ("    " * nestLevel) + "Global ID:", self.globalId
		print ("    " * nestLevel) + "Level:", self.level
		print ("    " * nestLevel) + "Matrix Width:", self.matrixWidth
		print ("    " * nestLevel) + "Initial Entropy:", self.initialEntropy
		print ("    " * nestLevel) + "Final Entropy:", self.initialEntropy
		#print ("    " * nestLevel), self.matrix
		for x in xrange(0, len(self.subMatrixAnalyses)):
			self.subMatrixAnalyses[x].printMatrixAnalysis(nestLevel = nestLevel + 1)
		
	
def getSubMatrices(inputMatrix):
	inputMatrixWidth = len(inputMatrix)
	subMatrices = []
	subMatrixWidth = inputMatrixWidth / 2
	
	subMatrices.append(inputMatrix[0 : subMatrixWidth, 0 : subMatrixWidth])
	subMatrices.append(inputMatrix[0 : subMatrixWidth, subMatrixWidth : inputMatrixWidth])
	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, 0 : subMatrixWidth])
	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, subMatrixWidth : inputMatrixWidth])
	return subMatrices

def bundleMatrices(matrices):
	matrixCount = len(matrices)
	if matrixCount != 4:
		raise ValueError("bundleMatrices expected 4 matrices, not" + str(matrixCount))
	topMatrices = numpy.concatenate((matrices[0], matrices[1]), axis = 1)
	bottomMatrices = numpy.concatenate((matrices[2], matrices[3]), axis = 1)
	outputMatrix = numpy.concatenate((topMatrices, bottomMatrices), axis = 0)
	return outputMatrix
	
#imageArray = exputils.getBitArrayFromBitmapFile("plus_sign_2.bmp")
#squareImageArray = exputils.unflattenArray(imageArray, 512)

inputWidth = 8192
input1 = exputils.getRandom2dBoolMatrix(inputWidth, inputWidth)
#
#for y in xrange(106, 406):
#	for x in xrange(226, 286):
#		input1[y, x] = 0
#
#for y in xrange(226, 286):
#	for x in xrange(106, 406):
#		input1[y, x] = 0
#
exputils.writeMatrixImage(input1, "input_1_raw.png")

inputData = input1
previousEntropy = -1
for cycle in xrange(0, 20):

	currentEntropy = exputils.calcEntropy(inputData.flatten())
	if previousEntropy != currentEntropy:
		previousEntropy = currentEntropy
		print "iteration", cycle, "initial entropy", currentEntropy
		mainMatrixAnalysis = MatrixAnalysis()
		mainMatrixAnalysis.process(matrix = inputData)
		print "iteration", cycle, "final entropy", mainMatrixAnalysis.finalEntropy
		exputils.writeMatrixImage(mainMatrixAnalysis.matrix, "input_1_red_" + str(cycle).zfill(5) + ".png")
		inputData = mainMatrixAnalysis.matrix

##inputData = exputils.getRandom2dBoolMatrix(inputWidth, inputWidth)
#
#
#testPicOriginal = exputils.getRandom2dBoolMatrix(inputWidth, inputWidth)
#testPicModified = testPicOriginal.copy()
#testPicModified = numpy.roll(testPicModified, shift = 4, axis = 0)
#testPicModified = numpy.roll(testPicModified, shift = 2, axis = 1)
#
#inputData = testPicOriginal
#previousEntropy = -1
#for cycle in xrange(0, 20):
#
#	currentEntropy = exputils.calcEntropy(inputData.flatten())
#	if previousEntropy != currentEntropy:
#		previousEntropy = currentEntropy
#		print "iteration", cycle, "initial entropy", currentEntropy
#		exputils.writeMatrixImage(inputData, "test_pic_original_symbol_gen_" + str(cycle).zfill(5) + ".png")
#			
#		mainMatrixAnalysis = MatrixAnalysis()
#		mainMatrixAnalysis.process(matrix = inputData)
#		print "iteration", cycle, "final entropy", mainMatrixAnalysis.finalEntropy
#		inputData = mainMatrixAnalysis.matrix
#
#originalPicSymbol = inputData
#inputData = testPicModified
#previousEntropy = -1
#for cycle in xrange(0, 20):
#
#	currentEntropy = exputils.calcEntropy(inputData.flatten())
#	if previousEntropy != currentEntropy:
#		previousEntropy = currentEntropy
#		print "iteration", cycle, "initial entropy", currentEntropy
#		exputils.writeMatrixImage(inputData, "test_pic_modified_symbol_gen_" + str(cycle).zfill(5) + ".png")
#			
#		mainMatrixAnalysis = MatrixAnalysis()
#		mainMatrixAnalysis.process(matrix = inputData)
#		print "iteration", cycle, "final entropy", mainMatrixAnalysis.finalEntropy
#		inputData = mainMatrixAnalysis.matrix
#
#modifiedPicSymbol = inputData
#symbolDiffXor = xorMatrices(originalPicSymbol, modifiedPicSymbol)
#
#exputils.writeMatrixImage(symbolDiffXor, "symbol_dif_xor.png")
#inputData = symbolDiffXor
#previousEntropy = -1
#for cycle in xrange(0, 20):
#
#	currentEntropy = exputils.calcEntropy(inputData.flatten())
#	if previousEntropy != currentEntropy:
#		previousEntropy = currentEntropy
#		print "iteration", cycle, "initial entropy", currentEntropy
#		exputils.writeMatrixImage(inputData, "xor_dif_reduction_gen_" + str(cycle).zfill(5) + ".png")
#			
#		mainMatrixAnalysis = MatrixAnalysis()
#		mainMatrixAnalysis.process(matrix = inputData)
#		print "iteration", cycle, "final entropy", mainMatrixAnalysis.finalEntropy
#		inputData = mainMatrixAnalysis.matrix
#
#modifiedPicSymbol = inputData
#symbolDiffXor = xorMatrices(originalPicSymbol, modifiedPicSymbol)
 
 
#previousEntropy = -1
#for cycle in xrange(0, 20):
#
#	currentEntropy = exputils.calcEntropy(inputData.flatten())
#	if previousEntropy != currentEntropy:
#		previousEntropy = currentEntropy
#		print "iteration", cycle, "initial entropy", currentEntropy
#		if generateOutputMovie:
#			exputils.writeMatrixImage(inputData, outputImagePrefix + str(cycle).zfill(5) + ".png")
#			
#		mainMatrixAnalysis = MatrixAnalysis()
#		mainMatrixAnalysis.process(matrix = inputData)
#		print "iteration", cycle, "final entropy", mainMatrixAnalysis.finalEntropy
#		inputData = mainMatrixAnalysis.matrix
#	
#if generateOutputMovie:
#	exputils.writeMatrixImage(mainMatrixAnalysis.matrix, outputImagePrefix + str(cycle).zfill(5) + ".png")
#
#if generateOutputMovie:
#	exputils.generateMovie(outputImageMask, outputImagePrefix + "movie.gif", fps = 5)
