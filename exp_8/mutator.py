import BitArray2D
import random as rnd
import matplotlib.pyplot as pyplot
import numpy
#import math
from matplotlib.pylab import *
#from scitools.std import *

def getRandomBitMatrix(width):
	data = BitArray2D.BitArray2D(rows = width, columns = width)
	for row in xrange(0, width):
		for col in xrange(0, width):
			data[row, col] = rnd.getrandbits(1)
	return data

def writeMatrixImage(matrix, filename):
	# copy BitArray2D matrix to numpy array
	data = numpy.empty(shape = (matrix.rows, matrix.columns), dtype = "bool")
	for row in xrange(0, matrix.rows):
		for col in xrange(0, matrix.columns):
			data[row, col] = matrix[BitArray2D.godel(row, col)]
	
	fig = pyplot.figure(figsize = (18, 18), dpi = 80)
	pyplot.cla()
	ms = matshow(data, fignum = False, cmap = cm.binary)
	fig.savefig(filename)
	pyplot.close()
	
class _Quadrant:
	def __init__(self, quadrantWidth, topCoordinate, leftCoordinate):
		self.quadrantWidth = quadrantWidth
		self.topCoordinate = topCoordinate
		self.leftCoordinate = leftCoordinate

class _Instructions:
	applyToQuadrant = None
	def __init__(self, applyOperation, applyFromQuadrant, applyToQuadrantIndex):
		self.applyOperation = applyOperation
		self.applyFromQuadrant = applyFromQuadrant
		self.applyToQuadrantIndex = applyToQuadrantIndex

class Mutator:

	andCalls = 0
	orCalls = 0
	xorCalls = 0
	sameCalls = 0
	noOpCalls = 0
	
	matrix = None
	possibleOperations = None
	quadrantIndexes = {
		"00": 0,
		"01": 1,
		"10": 2,
		"11": 3
	}
	
	def __init__(self, matrix):
		self.matrix = matrix
		self.possibleOperations = {
			#"00": self._operationAnd,
			#"01": self._operationOr,
			#"10": self._operationXor,
			#"11": self._operationSame
			"00": self._operationNoOp,
			"01": self._operationXor,
			"10": self._operationNoOp,
			"11": self._operationXor
		}

	def printOperationStats(self):
		print " and:", self.andCalls
		print "  or:", self.orCalls
		print " xor:", self.xorCalls
		print "same:", self.sameCalls
		print "noOp:", self.noOpCalls
		
	def mutate(self):
		self.andCalls = 0
		self.orCalls = 0
		self.xorCalls = 0
		self.sameCalls = 0
		self.noOpCalls = 0
		mainQuadrant = _Quadrant(quadrantWidth = self.matrix.columns, topCoordinate = 0, leftCoordinate = 0)
		finalInstructions = self._recursiveStep(level = 0, quadrant = mainQuadrant)
		return finalInstructions
		
	def _recursiveStep(self, level, quadrant):
		#print "entering recursive step, level =", level
		if quadrant.quadrantWidth > 2:
			instructionSet = []
			subQuadrants = self._getSubQuadrants(quadrant)
			for subQuadrant in subQuadrants:
				instructions = self._recursiveStep(level = level + 1, quadrant = subQuadrant)
				instructions.applyToQuadrant = subQuadrants[instructions.applyToQuadrantIndex]
				instructionSet.append(instructions)
				
			for instructions in instructionSet:
				self._applyInstructions(instructions = instructions)
			
		return self._getInstructionsFromQuadrant(quadrant = quadrant)

	def _getInstructionsFromQuadrant(self, quadrant):
		#print "entering getInstructionsFromQuadrant"
		subQuadrants = self._getSubQuadrants(quadrant = quadrant)
		#print "quad0Value =", self._getQuadrantValue(subQuadrants[0])
		#print "quad1Value =", self._getQuadrantValue(subQuadrants[1])
		#print "quad2Value =", self._getQuadrantValue(subQuadrants[2])
		#print "quad3Value =", self._getQuadrantValue(subQuadrants[3])
		applyOperation = self.possibleOperations[str(self._getQuadrantValue(subQuadrants[0])) + str(self._getQuadrantValue(subQuadrants[1]))]
		applyToQuadrantIndex = self.quadrantIndexes[str(self._getQuadrantValue(subQuadrants[2])) + str(self._getQuadrantValue(subQuadrants[3]))]
		
		return _Instructions(applyOperation = applyOperation, applyFromQuadrant = quadrant, applyToQuadrantIndex = applyToQuadrantIndex)
		
	def _applyInstructions(self, instructions):
		applyOperation = instructions.applyOperation
		applyFromQuadrantTopCoord = instructions.applyFromQuadrant.topCoordinate
		applyFromQuadrantLeftCoord = instructions.applyFromQuadrant.leftCoordinate
		applyToQuadrantTopCoord = instructions.applyToQuadrant.topCoordinate
		applyToQuadrantLeftCoord = instructions.applyToQuadrant.leftCoordinate
		quadrantWidth = instructions.applyFromQuadrant.quadrantWidth
		
		for row in xrange(0, quadrantWidth):
			fromRowCoord = applyFromQuadrantTopCoord + row
			toRowCoord = applyToQuadrantTopCoord + row
			for col in xrange(0, quadrantWidth):
				fromColCoord = applyFromQuadrantLeftCoord + col
				toColCoord = applyToQuadrantLeftCoord + col
				fromValue = self.matrix[BitArray2D.godel(fromRowCoord, fromColCoord)]
				toValue = self.matrix[BitArray2D.godel(toRowCoord, toColCoord)]
				self.matrix[toRowCoord, toColCoord] = applyOperation(leftBit = fromValue, rightBit = toValue)
				
	def _getSubQuadrantFromIndex(self, quadrant, subQuadrantIndex):
		subQuadrantWidth = quadrant.quadrantWidth / 2
		if subQuadrantIndex == 0:
			return _Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate, leftCoordinate = quadrant.leftCoordinate)
		elif subQuadrantIndex == 1:
			return _Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate, leftCoordinate = quadrant.leftCoordinate + subQuadrantWidth)
		elif subQuadrantIndex == 2:
			return _Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate + subQuadrantWidth, leftCoordinate = quadrant.leftCoordinate)
		elif subQuadrantIndex == 3:
			return _Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = quadrant.topCoordinate + subQuadrantWidth, leftCoordinate = quadrant.leftCoordinate + subQuadrantWidth)

	def _getSubQuadrants(self, quadrant):
		subQuadrants = []
		for subQuadrantIndex in xrange(0, 4):
			subQuadrants.append(self._getSubQuadrantFromIndex(quadrant = quadrant, subQuadrantIndex = subQuadrantIndex))
		
		return subQuadrants
	
	def _getQuadrantValue(self, quadrant):
		totalOnes = 0
		halfCount = (quadrant.quadrantWidth ** 2) / 2
		
		if halfCount < 1:
			return self.matrix[BitArray2D.godel(quadrant.topCoordinate, quadrant.leftCoordinate)]

		for row in xrange(0, quadrant.quadrantWidth):
			for column in xrange(0, quadrant.quadrantWidth):
				bitValue = self.matrix[BitArray2D.godel(quadrant.topCoordinate + row, quadrant.leftCoordinate + column)]
				if bitValue == 1:
					totalOnes += 1
				if totalOnes == halfCount:
					return 1
					
		return 0

	def _operationAnd(self, leftBit, rightBit):
		self.andCalls += 1
		return leftBit and rightBit
		
	def _operationOr(self, leftBit, rightBit):
		self.orCalls  += 1
		return leftBit or rightBit

	def _operationXor(self, leftBit, rightBit):
		self.xorCalls += 1
		return leftBit != rightBit

	def _operationSame(self, leftBit, rightBit):
		self.sameCalls += 1
		return leftBit == rightBit

	def _operationNoOp(self, leftBit, rightBit):
		self.noOpCalls += 1
		return rightBit
