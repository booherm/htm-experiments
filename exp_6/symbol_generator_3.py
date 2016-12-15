import exputils
import math
import numpy
import matplotlib.pyplot as pyplot
from bitvector import BitVector
from matplotlib.pylab import *

globalIdCounter = -1
def getGlobalId():
	global globalIdCounter
	globalIdCounter += 1
	return globalIdCounter

class _Quadrant:
	def __init__(self, quadrantWidth, topCoordinate, leftCoordinate, entropy = None):
		self.quadrantWidth = quadrantWidth
		self.topCoordinate = topCoordinate
		self.leftCoordinate = leftCoordinate
		self.entropy = entropy

class SymbolGenerator:
	
	def __init__(self, matrix, outputImageFilenamePrefix = None, maxIterations = 20):
		self.matrix = matrix[:]
		print "self.matrix:"
		print self.matrix
		self.outputImageFilenamePrefix = outputImageFilenamePrefix
		self.maxIterations = maxIterations
	
	def process(self):
		previousEntropy = None
		topLevelQuadrant = _Quadrant(quadrantWidth = len(self.matrix), topCoordinate = 0, leftCoordinate = 0)
		currentEntropy = self.__calcEntropy(quadrant = topLevelQuadrant)

		for iteration in xrange(0, self.maxIterations):
			#if previousEntropy is None or previousEntropy != currentEntropy:
			if self.outputImageFilenamePrefix is not None:
				self.__generateMatrixImage(filename = self.outputImageFilenamePrefix + str(iteration).zfill(5) + ".png")
			previousEntropy = currentEntropy
			print "iteration", iteration, "initial entropy =", currentEntropy
			currentEntropy = self.recursiveStep(quadrant = topLevelQuadrant, level = 0)
			print "iteration", iteration, "new entropy =", currentEntropy
	
	def recursiveStep(self, quadrant, level):

		initialEntropy = self.__calcEntropy(quadrant = quadrant)
		if quadrant.quadrantWidth > 2:   # entropy probabilities are evenly distributed <= 3 bits, no point splitting down further
		
			subQuadrantWidth = quadrant.quadrantWidth / 2
			subQuadrants = []
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate, leftCoordinate = quadrant.leftCoordinate))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate, leftCoordinate = quadrant.leftCoordinate + subQuadrantWidth))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate + subQuadrantWidth, leftCoordinate = quadrant.leftCoordinate))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate + subQuadrantWidth, leftCoordinate = quadrant.leftCoordinate + subQuadrantWidth))

			# determine winner sub quadrant
			winnerSubQuadrant = None
			for subQuadrant in subQuadrants:
				subQuadrantEntropy = self.recursiveStep(quadrant = subQuadrant, level = level + 1)
				if winnerSubQuadrant is None or subQuadrantEntropy < winnerSubQuadrant.entropy:
					winnerSubQuadrant = subQuadrant

			# xor winner with all peers and self last
			subQuadrantsXor = []
			for subQuadrant in subQuadrants:
				if subQuadrant != winnerSubQuadrant:
					subQuadrantsXor.append(subQuadrant)
			subQuadrantsXor.append(winnerSubQuadrant)
			for subQuadrant in subQuadrantsXor:
				self.__xorQuadrants(winnerQuadrant = winnerSubQuadrant, peerQuadrant = subQuadrant)

		finalEntropy = self.__calcEntropy(quadrant = quadrant)
		
		#return finalEntropy
		return initialEntropy
		
	def __calcEntropy(self, quadrant):
		matrixWidth = quadrant.quadrantWidth
		totalCount = matrixWidth * matrixWidth
		trueCount = 0
		for row in xrange(0, matrixWidth):
			for column in xrange(0, matrixWidth):
				if self.matrix[row, column]:
					trueCount = trueCount + 1
		falseCount = totalCount - trueCount

		pctFalse = float(falseCount) / totalCount
		pctTrue = float(trueCount) / totalCount
		if pctFalse == 1 or pctTrue == 1:
			entropy = 0
		else:
			entropy = -((math.log(pctFalse, 2) * pctFalse) + (math.log(pctTrue, 2) * pctTrue))
		
		return entropy
		
	def __generateMatrixImage(self, filename):
		fig = pyplot.figure(figsize = (18, 18), dpi = 80)
		pyplot.cla()
		ms = matshow(self.matrix, fignum = False, cmap = cm.binary)
		fig.savefig(filename)
		pyplot.close()

	def __xorQuadrants(self, winnerQuadrant, peerQuadrant):
		quadrantWidth = winnerQuadrant.quadrantWidth
		
		for row in xrange(0, quadrantWidth):
			for column in xrange(0, quadrantWidth):
				winnerTopCoordinate = winnerQuadrant.topCoordinate + row
				winnerLeftCoordinate = winnerQuadrant.leftCoordinate + column
				peerTopCoordinate = peerQuadrant.topCoordinate + row
				peerLeftCoordinate = peerQuadrant.leftCoordinate + column
				
				value = False
				if self.matrix[winnerTopCoordinate, winnerLeftCoordinate] != self.matrix[peerTopCoordinate, peerLeftCoordinate]:
					value = True
				self.matrix[peerTopCoordinate, peerLeftCoordinate] = value














#globalIdCounter = -1
#def getGlobalId():
#	global globalIdCounter
#	globalIdCounter += 1
#	return globalIdCounter
#
##------ simple xor of 2 matrices
#def xorMatrices(leftMatrix, rightMatrix):
#	length = len(leftMatrix)
#	outputData = numpy.empty(shape = (length, length), dtype = "bool")
#	for x in xrange(0, length):
#		for y in xrange(0, length):
#			value = False
#			if leftMatrix[x, y] != rightMatrix[x, y]:
#				value = True
#			outputData[x, y] = value
#
#	return outputData
#
##class SymbolGenerator:
##	level = None
##	initialEntropy = None
##	finalEntropy = None
##	matrixWidth = None
##	subSymbolGenerators = None
##	globalId = None
##	
##	def __init__(self, matrix, outputImageFilenamePrefix = None, maxIterations = 20):
##		self.matrix = matrix
##		self.outputImageFilenamePrefix = outputImageFilenamePrefix
##		self.maxIterations = maxIterations
##	
##	def process(self):
##		previousEntropy = -1
##		for cycle in xrange(0, self.maxIterations):
##			currentEntropy = self.__calcEntropy(matrix = self.matrix)
##			if previousEntropy != currentEntropy:
##				previousEntropy = currentEntropy
##				print "iteration", cycle, "initial entropy", currentEntropy
##				sg = self.recursiveStep(matrix = self.matrix, level = 0)
##				print "iteration", cycle, "final entropy", sg.finalEntropy
##				if self.outputImageFilenamePrefix is not None:
##					exputils.writeMatrixImage(sg.matrix, self.outputImageFilenamePrefix + str(cycle).zfill(5) + ".png")
##
##
##	
##	def recursiveStep(self, matrix, level = 0):
##		self.level = level
##		self.subSymbolGenerators = []
##		self.matrix = matrix
##		self.matrixWidth = len(matrix)
##
##		self.globalId = getGlobalId()
##		self.initialEntropy = self.__calcEntropy(matrix = self.matrix)
##		
##		#print ("    " * level), "processing globalId", self.globalId
##		
##		if self.matrixWidth > 1:   # we can further descend
##		
##			winnerMatrixAttributes = None
##			for subMatrix in getSubMatrices(self.matrix):
##			
##				# this could be done in parallel while this parent process blocks until its sub matrices are done
##				subSymbolGenerator = SymbolGenerator(matrix = subMatrix, outputImageFilenamePrefix = self.outputImageFilenamePrefix)
##				result = subSymbolGenerator.recursiveStep(matrix = subMatrix, level = level + 1)
##				self.subSymbolGenerators.append(result)
##				
##				if winnerMatrixAttributes is None or result.initialEntropy < winnerMatrixAttributes["initialEntropy"]:
##					winnerMatrixAttributes = {
##						"globalId":       result.globalId,
##						"matrix":         result.matrix,
##						"initialEntropy": result.initialEntropy
##					}
##
##			if winnerMatrixAttributes is None:
##				winner = self.subSymbolGenerators[0]
##				winnerMatrixAttributes = {
##					"globalId":       result.globalId,
##					"matrix":         result.matrix,
##					"initialEntropy": result.initialEntropy
##				}
##			
##			#print "determined level", level, winnerMatrixAttributes["globalId"], " entropy:", winnerMatrixAttributes["entropy"]
##			# xor winner with all peers, not self
##			for subSymbolGenerator in self.subSymbolGenerators:
##			#	#print ("    " * level), "    applying xor to ", subSymbolGenerator.globalId
##				#if subSymbolGenerator.globalId != winnerMatrixAttributes["globalId"]:
##				subSymbolGenerator.matrix = xorMatrices(winnerMatrixAttributes["matrix"], subSymbolGenerator.matrix)
##				subSymbolGenerator.finalEntropy = self.__calcEntropy(matrix = subSymbolGenerator.matrix)
##			
##			# bundle matrices and replace own matrix
##			newMatrices = []
##			for subSymbolGenerator in self.subSymbolGenerators:
##				newMatrices.append(subSymbolGenerator.matrix)
##			if len(newMatrices) != 0:
##				self.matrix = bundleMatrices(newMatrices)
##				self.finalEntropy = self.__calcEntropy(matrix = self.matrix)
##			else:
##				self.finalEntropy = self.initialEntropy
##			
##		return self
##		
##	def __calcEntropy(self, matrix):
##		matrixWidth = len(matrix)
##		totalCount = matrixWidth * matrixWidth
##		trueCount = 0
##		for y in xrange(0, matrixWidth):
##			for x in xrange(0, matrixWidth):
##				if matrix[y, x]:
##					trueCount = trueCount + 1
##		falseCount = totalCount - trueCount
##
##		pctFalse = float(falseCount) / totalCount
##		pctTrue = float(trueCount) / totalCount
##		if pctFalse == 1 or pctTrue == 1:
##			entropy = 0
##		else:
##			entropy = -((math.log(pctFalse, 2) * pctFalse) + (math.log(pctTrue, 2) * pctTrue))
##		
##		return entropy
##
##def getSubMatrices(inputMatrix):
##	inputMatrixWidth = len(inputMatrix)
##	subMatrices = []
##	subMatrixWidth = inputMatrixWidth / 2
##	
##	subMatrices.append(inputMatrix[0 : subMatrixWidth, 0 : subMatrixWidth])
##	subMatrices.append(inputMatrix[0 : subMatrixWidth, subMatrixWidth : inputMatrixWidth])
##	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, 0 : subMatrixWidth])
##	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, subMatrixWidth : inputMatrixWidth])
##	return subMatrices
##
##def bundleMatrices(matrices):
##	matrixCount = len(matrices)
##	if matrixCount != 4:
##		raise ValueError("bundleMatrices expected 4 matrices, not" + str(matrixCount))
##	topMatrices = numpy.concatenate((matrices[0], matrices[1]), axis = 1)
##	bottomMatrices = numpy.concatenate((matrices[2], matrices[3]), axis = 1)
##	outputMatrix = numpy.concatenate((topMatrices, bottomMatrices), axis = 0)
##	return outputMatrix
##
##
##
##	
##	
##	
#	
#	
#	
#	
#	
#	
#globalIdCounter = -1
#def getGlobalId():
#	global globalIdCounter
#	globalIdCounter += 1
#	return globalIdCounter
#
##------ simple xor of 2 matrices
#def xorMatrices(leftMatrix, rightMatrix):
#	length = len(leftMatrix)
#	outputData = numpy.empty(shape = (length, length), dtype = "bool")
#	for x in xrange(0, length):
#		for y in xrange(0, length):
#			value = False
#			if leftMatrix[x, y] != rightMatrix[x, y]:
#				value = True
#			outputData[x, y] = value
#
#	return outputData
#
#class SymbolGenerator:
#	level = None
#	initialEntropy = None
#	finalEntropy = None
#	matrixWidth = None
#	subSymbolGenerators = None
#	globalId = None
#	
#	def __init__(self, matrix, outputImageFilenamePrefix = None, maxIterations = 20):
#		self.matrix = matrix
#		self.outputImageFilenamePrefix = outputImageFilenamePrefix
#		self.maxIterations = maxIterations
#	
#	def process(self):
#		previousEntropy = -1
#		for cycle in xrange(0, self.maxIterations):
#			currentEntropy = self.__calcEntropy(matrix = self.matrix)
#			if previousEntropy != currentEntropy:
#				previousEntropy = currentEntropy
#				print "iteration", cycle, "initial entropy", currentEntropy
#				sg = self.recursiveStep(matrix = self.matrix, level = 0)
#				print "iteration", cycle, "final entropy", sg.finalEntropy
#				if self.outputImageFilenamePrefix is not None:
#					exputils.writeMatrixImage(sg.matrix, self.outputImageFilenamePrefix + str(cycle).zfill(5) + ".png")
#
#
#	
#	def recursiveStep(self, matrix, level = 0):
#		self.level = level
#		self.subSymbolGenerators = []
#		self.matrix = matrix
#		self.matrixWidth = len(matrix)
#
#		self.globalId = getGlobalId()
#		self.initialEntropy = self.__calcEntropy(matrix = self.matrix)
#		
#		#print ("    " * level), "processing globalId", self.globalId
#		
#		if self.matrixWidth > 1:   # we can further descend
#		
#			winnerMatrixAttributes = None
#			for subMatrix in getSubMatrices(self.matrix):
#			
#				# this could be done in parallel while this parent process blocks until its sub matrices are done
#				subSymbolGenerator = SymbolGenerator(matrix = subMatrix, outputImageFilenamePrefix = self.outputImageFilenamePrefix)
#				result = subSymbolGenerator.recursiveStep(matrix = subMatrix, level = level + 1)
#				self.subSymbolGenerators.append(result)
#				
#				if winnerMatrixAttributes is None or result.initialEntropy < winnerMatrixAttributes["initialEntropy"]:
#					winnerMatrixAttributes = {
#						"globalId":       result.globalId,
#						"matrix":         result.matrix,
#						"initialEntropy": result.initialEntropy
#					}
#
#			if winnerMatrixAttributes is None:
#				winner = self.subSymbolGenerators[0]
#				winnerMatrixAttributes = {
#					"globalId":       result.globalId,
#					"matrix":         result.matrix,
#					"initialEntropy": result.initialEntropy
#				}
#			
#			#print "determined level", level, winnerMatrixAttributes["globalId"], " entropy:", winnerMatrixAttributes["entropy"]
#			# xor winner with all peers, not self
#			for subSymbolGenerator in self.subSymbolGenerators:
#			#	#print ("    " * level), "    applying xor to ", subSymbolGenerator.globalId
#				#if subSymbolGenerator.globalId != winnerMatrixAttributes["globalId"]:
#				subSymbolGenerator.matrix = xorMatrices(winnerMatrixAttributes["matrix"], subSymbolGenerator.matrix)
#				subSymbolGenerator.finalEntropy = self.__calcEntropy(matrix = subSymbolGenerator.matrix)
#			
#			# bundle matrices and replace own matrix
#			newMatrices = []
#			for subSymbolGenerator in self.subSymbolGenerators:
#				newMatrices.append(subSymbolGenerator.matrix)
#			if len(newMatrices) != 0:
#				self.matrix = bundleMatrices(newMatrices)
#				self.finalEntropy = self.__calcEntropy(matrix = self.matrix)
#			else:
#				self.finalEntropy = self.initialEntropy
#			
#		return self
#		
#	def __calcEntropy(self, matrix):
#		matrixWidth = len(matrix)
#		totalCount = matrixWidth * matrixWidth
#		trueCount = 0
#		for y in xrange(0, matrixWidth):
#			for x in xrange(0, matrixWidth):
#				if matrix[y, x]:
#					trueCount = trueCount + 1
#		falseCount = totalCount - trueCount
#
#		pctFalse = float(falseCount) / totalCount
#		pctTrue = float(trueCount) / totalCount
#		if pctFalse == 1 or pctTrue == 1:
#			entropy = 0
#		else:
#			entropy = -((math.log(pctFalse, 2) * pctFalse) + (math.log(pctTrue, 2) * pctTrue))
#		
#		return entropy
#
#def getSubMatrices(inputMatrix):
#	inputMatrixWidth = len(inputMatrix)
#	subMatrices = []
#	subMatrixWidth = inputMatrixWidth / 2
#	
#	subMatrices.append(inputMatrix[0 : subMatrixWidth, 0 : subMatrixWidth])
#	subMatrices.append(inputMatrix[0 : subMatrixWidth, subMatrixWidth : inputMatrixWidth])
#	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, 0 : subMatrixWidth])
#	subMatrices.append(inputMatrix[subMatrixWidth : inputMatrixWidth, subMatrixWidth : inputMatrixWidth])
#	return subMatrices
#
#def bundleMatrices(matrices):
#	matrixCount = len(matrices)
#	if matrixCount != 4:
#		raise ValueError("bundleMatrices expected 4 matrices, not" + str(matrixCount))
#	topMatrices = numpy.concatenate((matrices[0], matrices[1]), axis = 1)
#	bottomMatrices = numpy.concatenate((matrices[2], matrices[3]), axis = 1)
#	outputMatrix = numpy.concatenate((topMatrices, bottomMatrices), axis = 0)
#	return outputMatrix
#
#
#