import BitArray2D
import hashlib
import random as rnd
import matplotlib.pyplot as pyplot
import math
import numpy
from matplotlib.pylab import *

nandResults = {
	"0001_1110": "dec",
	"0010_1101": "dec",
	"0011_0100": "dec",
	"0011_1000": "dec",
	"0011_1100": "dec",
	"0011_1101": "dec",
	"0011_1110": "dec",
	"0100_1011": "dec",
	"0101_1000": "dec",
	"0101_1010": "dec",
	"0101_1011": "dec",
	"0101_1110": "dec",
	"0110_1000": "dec",
	"0110_1001": "dec",
	"0110_1011": "dec",
	"0110_1101": "dec",
	"0111_1000": "dec",
	"1001_1110": "dec",
	"1010_1101": "dec",
	"0001_0010": "dec",
	"0001_0100": "dec",
	"0001_1000": "dec",
	"0010_0100": "dec",
	"0010_1000": "dec",
	"0100_1000": "dec",
	"0011_0101": "dec",
	"0011_0110": "dec",
	"0011_1001": "dec",
	"0011_1010": "dec",
	"0101_0110": "dec",
	"0101_1001": "dec",
	"0101_1100": "dec",
	"0110_1010": "dec",
	"0110_1100": "dec",
	"1001_1010": "dec",
	"1001_1100": "dec",
	"1010_1100": "dec",
	"0001_0110": "dec",
	"0001_1010": "dec",
	"0001_1100": "dec",
	"0010_0101": "dec",
	"0010_1001": "dec",
	"0010_1100": "dec",
	"0100_1001": "dec",
	"0100_1010": "dec",
	"0111_1011": "inc",
	"0111_1101": "inc",
	"0111_1110": "inc",
	"1011_1101": "inc",
	"1011_1110": "inc",
	"1101_1110": "inc"
}

xorResults = {
	"0000_0000": "same",
	"0000_0001": "inc",
	"0000_0010": "inc",
	"0000_0011": "inc",
	"0000_0100": "inc",
	"0000_0101": "inc",
	"0000_0110": "inc",
	"0000_0111": "inc",
	"0000_1000": "inc",
	"0000_1001": "inc",
	"0000_1010": "inc",
	"0000_1011": "inc",
	"0000_1100": "inc",
	"0000_1101": "inc",
	"0000_1110": "inc",
	"0000_1111": "same",
	"0001_0000": "same",
	"0001_0001": "dec",
	"0001_0010": "inc",
	"0001_0011": "same",
	"0001_0100": "inc",
	"0001_0101": "same",
	"0001_0110": "same",
	"0001_0111": "inc",
	"0001_1000": "inc",
	"0001_1001": "same",
	"0001_1010": "same",
	"0001_1011": "inc",
	"0001_1100": "same",
	"0001_1101": "inc",
	"0001_1110": "dec",
	"0001_1111": "same",
	"0010_0000": "same",
	"0010_0001": "inc",
	"0010_0010": "dec",
	"0010_0011": "same",
	"0010_0100": "inc",
	"0010_0101": "same",
	"0010_0110": "same",
	"0010_0111": "inc",
	"0010_1000": "inc",
	"0010_1001": "same",
	"0010_1010": "same",
	"0010_1011": "inc",
	"0010_1100": "same",
	"0010_1101": "dec",
	"0010_1110": "inc",
	"0010_1111": "same",
	"0011_0000": "same",
	"0011_0001": "dec",
	"0011_0010": "dec",
	"0011_0011": "dec",
	"0011_0100": "dec",
	"0011_0101": "same",
	"0011_0110": "same",
	"0011_0111": "dec",
	"0011_1000": "dec",
	"0011_1001": "same",
	"0011_1010": "same",
	"0011_1011": "dec",
	"0011_1100": "dec",
	"0011_1101": "dec",
	"0011_1110": "dec",
	"0011_1111": "same",
	"0100_0000": "same",
	"0100_0001": "inc",
	"0100_0010": "inc",
	"0100_0011": "same",
	"0100_0100": "dec",
	"0100_0101": "same",
	"0100_0110": "same",
	"0100_0111": "inc",
	"0100_1000": "inc",
	"0100_1001": "same",
	"0100_1010": "same",
	"0100_1011": "dec",
	"0100_1100": "same",
	"0100_1101": "inc",
	"0100_1110": "inc",
	"0100_1111": "same",
	"0101_0000": "same",
	"0101_0001": "dec",
	"0101_0010": "dec",
	"0101_0011": "same",
	"0101_0100": "dec",
	"0101_0101": "dec",
	"0101_0110": "same",
	"0101_0111": "dec",
	"0101_1000": "dec",
	"0101_1001": "same",
	"0101_1010": "dec",
	"0101_1011": "dec",
	"0101_1100": "same",
	"0101_1101": "dec",
	"0101_1110": "dec",
	"0101_1111": "same",
	"0110_0000": "same",
	"0110_0001": "dec",
	"0110_0010": "dec",
	"0110_0011": "same",
	"0110_0100": "dec",
	"0110_0101": "same",
	"0110_0110": "dec",
	"0110_0111": "dec",
	"0110_1000": "dec",
	"0110_1001": "dec",
	"0110_1010": "same",
	"0110_1011": "dec",
	"0110_1100": "same",
	"0110_1101": "dec",
	"0110_1110": "dec",
	"0110_1111": "same",
	"0111_0000": "same",
	"0111_0001": "inc",
	"0111_0010": "inc",
	"0111_0011": "same",
	"0111_0100": "inc",
	"0111_0101": "same",
	"0111_0110": "same",
	"0111_0111": "dec",
	"0111_1000": "dec",
	"0111_1001": "same",
	"0111_1010": "same",
	"0111_1011": "inc",
	"0111_1100": "same",
	"0111_1101": "inc",
	"0111_1110": "inc",
	"0111_1111": "same",
	"1000_0000": "same",
	"1000_0001": "inc",
	"1000_0010": "inc",
	"1000_0011": "same",
	"1000_0100": "inc",
	"1000_0101": "same",
	"1000_0110": "same",
	"1000_0111": "dec",
	"1000_1000": "dec",
	"1000_1001": "same",
	"1000_1010": "same",
	"1000_1011": "inc",
	"1000_1100": "same",
	"1000_1101": "inc",
	"1000_1110": "inc",
	"1000_1111": "same",
	"1001_0000": "same",
	"1001_0001": "dec",
	"1001_0010": "dec",
	"1001_0011": "same",
	"1001_0100": "dec",
	"1001_0101": "same",
	"1001_0110": "dec",
	"1001_0111": "dec",
	"1001_1000": "dec",
	"1001_1001": "dec",
	"1001_1010": "same",
	"1001_1011": "dec",
	"1001_1100": "same",
	"1001_1101": "dec",
	"1001_1110": "dec",
	"1001_1111": "same",
	"1010_0000": "same",
	"1010_0001": "dec",
	"1010_0010": "dec",
	"1010_0011": "same",
	"1010_0100": "dec",
	"1010_0101": "dec",
	"1010_0110": "same",
	"1010_0111": "dec",
	"1010_1000": "dec",
	"1010_1001": "same",
	"1010_1010": "dec",
	"1010_1011": "dec",
	"1010_1100": "same",
	"1010_1101": "dec",
	"1010_1110": "dec",
	"1010_1111": "same",
	"1011_0000": "same",
	"1011_0001": "inc",
	"1011_0010": "inc",
	"1011_0011": "same",
	"1011_0100": "dec",
	"1011_0101": "same",
	"1011_0110": "same",
	"1011_0111": "inc",
	"1011_1000": "inc",
	"1011_1001": "same",
	"1011_1010": "same",
	"1011_1011": "dec",
	"1011_1100": "same",
	"1011_1101": "inc",
	"1011_1110": "inc",
	"1011_1111": "same",
	"1100_0000": "same",
	"1100_0001": "dec",
	"1100_0010": "dec",
	"1100_0011": "dec",
	"1100_0100": "dec",
	"1100_0101": "same",
	"1100_0110": "same",
	"1100_0111": "dec",
	"1100_1000": "dec",
	"1100_1001": "same",
	"1100_1010": "same",
	"1100_1011": "dec",
	"1100_1100": "dec",
	"1100_1101": "dec",
	"1100_1110": "dec",
	"1100_1111": "same",
	"1101_0000": "same",
	"1101_0001": "inc",
	"1101_0010": "dec",
	"1101_0011": "same",
	"1101_0100": "inc",
	"1101_0101": "same",
	"1101_0110": "same",
	"1101_0111": "inc",
	"1101_1000": "inc",
	"1101_1001": "same",
	"1101_1010": "same",
	"1101_1011": "inc",
	"1101_1100": "same",
	"1101_1101": "dec",
	"1101_1110": "inc",
	"1101_1111": "same",
	"1110_0000": "same",
	"1110_0001": "dec",
	"1110_0010": "inc",
	"1110_0011": "same",
	"1110_0100": "inc",
	"1110_0101": "same",
	"1110_0110": "same",
	"1110_0111": "inc",
	"1110_1000": "inc",
	"1110_1001": "same",
	"1110_1010": "same",
	"1110_1011": "inc",
	"1110_1100": "same",
	"1110_1101": "inc",
	"1110_1110": "dec",
	"1110_1111": "same",
	"1111_0000": "same",
	"1111_0001": "inc",
	"1111_0010": "inc",
	"1111_0011": "inc",
	"1111_0100": "inc",
	"1111_0101": "inc",
	"1111_0110": "inc",
	"1111_0111": "inc",
	"1111_1000": "inc",
	"1111_1001": "inc",
	"1111_1010": "inc",
	"1111_1011": "inc",
	"1111_1100": "inc",
	"1111_1101": "inc",
	"1111_1110": "inc",
	"1111_1111": "same"
}

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

class Mutator:
	
	matrix = None
	topLevelInstructions = None
	targetEntropy = None
	desiredEntropyChange = None
	operator = "XOR"
	
	def __init__(self, matrix, topLevelInstructions, targetEntropy):
		self.matrix = matrix
		self.topLevelInstructions = topLevelInstructions
		self.targetEntropy = targetEntropy
	
	def mutate(self):
		mainQuadrant = _Quadrant(quadrantWidth = self.matrix.columns, topCoordinate = 0, leftCoordinate = 0)
		currentEntropy = self._getQuadrantEntropy(quadrant = mainQuadrant)
		self.desiredEntropyChange = self._getDesiredEntropyChange(currentEntropy = currentEntropy)
		print "    begin mutate, entropy =", currentEntropy, " topLevelInstructions =", self.topLevelInstructions, " desiredEntropyChange =", self.desiredEntropyChange
		finalInstructions = self._recursiveStep(level = 0, quadrant = mainQuadrant)
		print "    end mutate, finalInstructions =", finalInstructions
		self.topLevelInstructions = finalInstructions
		
	def getSha1Hash(self):
		m = hashlib.sha1()
		m.update(str(self.matrix))
		return m.hexdigest()
		
	def _recursiveStep(self, level, quadrant):
		if quadrant.quadrantWidth > 2:
			resultInstructions = ""
			subQuadrants = self._getSubQuadrants(quadrant = quadrant)
			for subQuadrant in subQuadrants:
				resultInstructions += self._recursiveStep(level = level + 1, quadrant = subQuadrant)
			#print "        collected resultInstructions = ", resultInstructions
			change = self._getOperatorEntropyChange(operator = self.operator, leftOperand = resultInstructions, rightOperand = self.topLevelInstructions)
			#print "        processed instructions against top level instructions, change = " + change
			if level == 0:
				#print "    level 0 return, change =", change
				if change == self.desiredEntropyChange:
					return self._getOperatorChange(operator = self.operator, leftOperand = resultInstructions, rightOperand = self.topLevelInstructions)
				else:
					return self.topLevelInstructions
			
			if change == self.desiredEntropyChange:
				return "1"
			
		else:
			change = self._getOperatorEntropyChange(operator = self.operator, leftOperand = self._getQuadrantString(quadrant = quadrant), rightOperand = self.topLevelInstructions)
			#print "        bottom level, change =", change
			if change == self.desiredEntropyChange:
				self._applyOperatorChange(operator = self.operator, quadrant = quadrant, rightOperand = self.topLevelInstructions)
				return "1"
			
		return "0"

	def _getQuadrantEntropy(self, quadrant):
		topCoord = quadrant.topCoordinate
		leftCoord = quadrant.leftCoordinate
		quadrantWidth = quadrant.quadrantWidth
		zeros = 0
		for row in xrange(topCoord, topCoord + quadrantWidth):
			for col in xrange(leftCoord, leftCoord + quadrantWidth):
				if self.matrix[BitArray2D.godel(row, col)] == 0:
					zeros = zeros + 1

		length = quadrantWidth ** 2
		ones = length - zeros
		pctZeros = float(zeros) / length
		pctOnes = float(ones) / length
		if pctZeros == 1 or pctOnes == 1:
			entropy = 0
		else:
			entropy = -((math.log(pctZeros, 2) * pctZeros) + (math.log(pctOnes, 2) * pctOnes))
		return entropy
	
	def _getDesiredEntropyChange(self, currentEntropy):
		if currentEntropy > self.targetEntropy:
			return "dec"
		return "inc"
		
	def _getQuadrantString(self, quadrant):
		topCoord = quadrant.topCoordinate
		leftCoord = quadrant.leftCoordinate

		quadString = ""
		for row in xrange(topCoord, topCoord + 2):
			for col in xrange(leftCoord, leftCoord + 2):
				quadString += str(self.matrix[BitArray2D.godel(row, col)])

		return quadString

	def _getOperatorEntropyChange(self, operator, leftOperand, rightOperand):
		global nandResults
		global xorResults
		
		if operator == "NAND":
			change = nandResults.get(leftOperand + "_" + rightOperand)
		elif operator == "XOR":
			change = xorResults.get(leftOperand + "_" + rightOperand)

		if change is None:
			return "same"
			#return self.desiredEntropyChange
			
		return change

	def _getOperatorChange(self, operator, leftOperand, rightOperand):
		result = ""
		for i in xrange(0, 4):
			result += str(self._getBooleanOperationValue(operator = operator, leftOperand = leftOperand[i], rightOperand = rightOperand[i]))

		return result

	def _applyOperatorChange(self, operator, quadrant, rightOperand):
		applyToQuadrantTopCoord = quadrant.topCoordinate
		applyToQuadrantLeftCoord = quadrant.leftCoordinate
		
		rightOperandIndex = 0
		for row in xrange(applyToQuadrantTopCoord, applyToQuadrantTopCoord + 2):
			for col in xrange(applyToQuadrantLeftCoord, applyToQuadrantLeftCoord + 2):
				leftValue = self.matrix[BitArray2D.godel(row, col)]
				rightValue = rightOperand[rightOperandIndex]
				setValue = self._getBooleanOperationValue(operator = operator, leftOperand = leftValue, rightOperand = rightValue)
				self.matrix[row, col] = setValue
				rightOperandIndex = rightOperandIndex + 1
				
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
		
	def _getBooleanOperationValue(self, operator, leftOperand, rightOperand):
		returnValue = None
		
		if operator == "NAND":
			returnValue = 1
			if leftOperand == rightOperand and leftOperand == "1":
				returnValue = 0
				
		elif operator == "XOR":
			returnValue = 0
			if leftOperand != rightOperand:
				returnValue = 1
				
		return returnValue
			
	
