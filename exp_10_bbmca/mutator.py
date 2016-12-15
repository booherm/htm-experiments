import BitArray2D
import hashlib
import random as rnd
import math
import image_utils

fredkinRules = {
	"0000": "0000",
	"0110": "1001",
	"1101": "1101",
	"0010": "0100",
	"0101": "0101",
	"1111": "1111",
	"1001": "0110",
	"0111": "0111",
	"1011": "1011",
	"1110": "1110",
	"1000": "0001",
	"0100": "0010",
	"0001": "1000",
	"1010": "1010",
	"1100": "1100",
	"0011": "0011"
}

def getRandomBitMatrix(width):
	data = BitArray2D.BitArray2D(rows = width, columns = width)
	for row in xrange(0, width):
		for col in xrange(0, width):
			data[row, col] = rnd.getrandbits(1)
	return data

class _Neighborhood:
	def __init__(self, neighborhoodWidth, topCoordinate, leftCoordinate):
		self.neighborhoodWidth = neighborhoodWidth
		self.topCoordinate = topCoordinate
		self.leftCoordinate = leftCoordinate

class Mutator:
	
	matrix = None
	topLevelInstructions = None
	topLevelWidth = None
	iteration = None
	
	def __init__(self, matrix, topLevelInstructions):
		self.matrix = matrix
		self.topLevelInstructions = topLevelInstructions
		self.topLevelWidth = matrix.columns
	
	def mutate(self, iteration):
	
		self.iteration = iteration
		
		mainNeighborhood = _Neighborhood(neighborhoodWidth = self.matrix.columns, topCoordinate = 0, leftCoordinate = 0)
		#currentEntropy = self._getNeighborhoodEntropy(neighborhood = mainNeighborhood)
		
		#print "    begin mutate, entropy =", currentEntropy
		
		evenFinalInstructions = self._recursiveStep(level = 0, neighborhood = mainNeighborhood, oddEven = "EVEN")
		image_utils.writeBitArray2DImage(bitArray = self.matrix, filename = str(self.iteration).zfill(5) + "_even.png")
		
		oddFinalInstructions = self._recursiveStep(level = 0, neighborhood = mainNeighborhood, oddEven = "ODD")
		image_utils.writeBitArray2DImage(bitArray = self.matrix, filename = str(self.iteration).zfill(5) + "_odd.png")
		
		finalInstructions = evenFinalInstructions + oddFinalInstructions
	#	print "    end mutate, finalInstructions =", finalInstructions
		
		self.topLevelInstructions = finalInstructions
		
	def getSha1Hash(self):
		m = hashlib.sha1()
		m.update(str(self.matrix))
		return m.hexdigest()
		
	def _recursiveStep(self, level, neighborhood, oddEven):
		if neighborhood.neighborhoodWidth > 2:
			resultInstructions = []
			subNeighborhoods = self._getSubNeighborhoods(neighborhood = neighborhood)
			for subNeighborhood in subNeighborhoods:
				resultInstructions.append(self._recursiveStep(level = level + 1, neighborhood = subNeighborhood, oddEven = oddEven))

			return resultInstructions
			
		else:
			self._applyNeighborhoodChange(neighborhood = neighborhood, step = oddEven)
			return "0"
			
		return "0"

	def _getNeighborhoodEntropy(self, neighborhood):
		topCoord = neighborhood.topCoordinate
		leftCoord = neighborhood.leftCoordinate
		neighborhoodWidth = neighborhood.neighborhoodWidth
		zeros = 0
		for row in xrange(topCoord, topCoord + neighborhoodWidth):
			for col in xrange(leftCoord, leftCoord + neighborhoodWidth):
				if self.matrix[BitArray2D.godel(row, col)] == 0:
					zeros = zeros + 1

		length = neighborhoodWidth ** 2
		ones = length - zeros
		pctZeros = float(zeros) / length
		pctOnes = float(ones) / length
		if pctZeros == 1 or pctOnes == 1:
			entropy = 0
		else:
			entropy = -((math.log(pctZeros, 2) * pctZeros) + (math.log(pctOnes, 2) * pctOnes))
		return entropy
		
	def _applyNeighborhoodChange(self, neighborhood, step):
		if step == "EVEN":
			aRow = neighborhood.topCoordinate
			aCol = neighborhood.leftCoordinate
			bRow = neighborhood.topCoordinate
			bCol = neighborhood.leftCoordinate + 1
			cRow = neighborhood.topCoordinate + 1
			cCol = neighborhood.leftCoordinate
			dRow = neighborhood.topCoordinate + 1
			dCol = neighborhood.leftCoordinate + 1
			aVal = str(self.matrix[BitArray2D.godel(aRow, aCol)])
			bVal = str(self.matrix[BitArray2D.godel(bRow, bCol)])
			cVal = str(self.matrix[BitArray2D.godel(cRow, cCol)])
			dVal = str(self.matrix[BitArray2D.godel(dRow, dCol)])
			currentState = aVal + bVal + cVal + dVal
			newState = fredkinRules[currentState]
			aVal = newState[0]
			bVal = newState[1]
			cVal = newState[2]
			dVal = newState[3]
			self.matrix[aRow, aCol] = int(aVal)
			self.matrix[bRow, bCol] = int(bVal)
			self.matrix[cRow, cCol] = int(cVal)
			self.matrix[dRow, dCol] = int(dVal)
			
		else:
			aRow = neighborhood.topCoordinate + 1
			aCol = neighborhood.leftCoordinate + 1
			bRow = neighborhood.topCoordinate + 1
			bCol = neighborhood.leftCoordinate + 1 + 1
			cRow = neighborhood.topCoordinate + 1 + 1
			cCol = neighborhood.leftCoordinate + 1
			dRow = neighborhood.topCoordinate + 1 + 1
			dCol = neighborhood.leftCoordinate + 1 + 1
			
			aVal = str(self.matrix[BitArray2D.godel(aRow, aCol)])
			if bCol >= self.topLevelWidth:
				bVal = "1"
			else:
				bVal = str(self.matrix[BitArray2D.godel(bRow, bCol)])
			
			if cRow >= self.topLevelWidth:
				cVal = "1"
			else:
				cVal = str(self.matrix[BitArray2D.godel(cRow, cCol)])
				
			if dRow >= self.topLevelWidth or dCol >= self.topLevelWidth:
				dVal = "1"
			else:
				dVal = str(self.matrix[BitArray2D.godel(dRow, dCol)])

			currentState = aVal + bVal + cVal + dVal
			newState = fredkinRules[currentState]
			aVal = newState[0]
			bVal = newState[1]
			cVal = newState[2]
			dVal = newState[3]

			self.matrix[aRow, aCol] = int(aVal)
			if bCol < self.topLevelWidth:
				self.matrix[bRow, bCol] = int(bVal)
			
			if cRow < self.topLevelWidth:
				self.matrix[cRow, cCol] = int(cVal)
				
			if dRow < self.topLevelWidth and dCol < self.topLevelWidth:
				self.matrix[dRow, dCol] = int(dVal)
			
			
	def _getSubNeighborhoodFromIndex(self, neighborhood, subNeighborhoodIndex):
		subNeighborhoodWidth = neighborhood.neighborhoodWidth / 2
		if subNeighborhoodIndex == 0:
			return _Neighborhood(neighborhoodWidth = subNeighborhoodWidth, topCoordinate = neighborhood.topCoordinate, leftCoordinate = neighborhood.leftCoordinate)
		elif subNeighborhoodIndex == 1:
			return _Neighborhood(neighborhoodWidth = subNeighborhoodWidth, topCoordinate = neighborhood.topCoordinate, leftCoordinate = neighborhood.leftCoordinate + subNeighborhoodWidth)
		elif subNeighborhoodIndex == 2:
			return _Neighborhood(neighborhoodWidth = subNeighborhoodWidth, topCoordinate = neighborhood.topCoordinate + subNeighborhoodWidth, leftCoordinate = neighborhood.leftCoordinate)
		elif subNeighborhoodIndex == 3:
			return _Neighborhood(neighborhoodWidth = subNeighborhoodWidth, topCoordinate = neighborhood.topCoordinate + subNeighborhoodWidth, leftCoordinate = neighborhood.leftCoordinate + subNeighborhoodWidth)
		

	def _getSubNeighborhoods(self, neighborhood):
		subNeighborhoods = []
		for subNeighborhoodIndex in xrange(0, 4):
			subNeighborhoods.append(self._getSubNeighborhoodFromIndex(neighborhood = neighborhood, subNeighborhoodIndex = subNeighborhoodIndex))
		
		return subNeighborhoods
		
