"""Matt's general intelligence symbol generator main class

MB 2015-05-28

"""

import exputils
import numpy

# TODO
# - no need to copy the sub matrices around, just manipulate one master matrix
# - log status and states to database for analysis, plain text print out is hard to read
# - parallelization
# - change datatype to bool in matrices for memory efficiency
# - use numpy xor function when values are bool
# - pass unflattened matrix to entropy calc
# - add in metric entropy everywhere
# - in case of tie entropy, the algorithm is taking the first min encountered, introducing some bias.
# - 	Change to sort, tie break on:
# -     1) if the matrices are the same, look at matrix layout.  Use matrix values to determine winner
# -     or 2) random - less preferred as we can give the algorithm more choice

#--------------------------------------- image / movie output setup  ----------------------------------

globalIdCounter = -1

def getGlobalId():
	global globalIdCounter
	globalIdCounter += 1
	return globalIdCounter

class SymbolGenerator:
	level = None
	initialEntropy = None
	finalEntropy = None
	matrix = None
	matrixWidth = None
	subSymbolGenerators = None
	globalId = None
	
	def process(self, matrix, level = 0, maxIterations = 20):
		self.level = level
		self.subSymbolGenerators = []
		self.matrix = matrix
		self.matrixWidth = len(matrix)
		self.globalId = getGlobalId()
		self.initialEntropy = exputils.calcEntropy(self.matrix.flatten())["entropy"]
		
		previousEntropy = -1
		for x in xrange(0, maxIterations): # maxIterations passes over the data should get it to a stable entropy.  Break out early if it stabilizes less than max
			exputils.writeMatrixImage(self.matrix, "sg_test_pic_" + str(x).zfill(5) + ".png")
			self.iterate()
			currentEntropy = exputils.calcEntropy(self.matrix.flatten())
			if currentEntropy == previousEntropy:
				break
			else:
				previousEntropy = currentEntropy
			
		return self

	def iterate(self, level = 0):
		
		if self.matrixWidth > 1:   # we can further descend
			winnerMatrixAttributes = None
			for subMatrix in getSubMatrices(self.matrix):
			
				# this could be done in parallel while this parent process blocks until its sub matrices are done
				subSymbolGenerator = SymbolGenerator()
				result = subSymbolGenerator.process(matrix = subMatrix, level = level + 1)
				self.subSymbolGenerators.append(result)
				
				# the winner sub-matrix is the one with the least entropy
				# ???? in case of a tie, the first one in sequence is selected as the winner.  This will add some bias.
				# ???? is there other information we can utilize to determine which of the n winners to select?
				if winnerMatrixAttributes is None or result.initialEntropy < winnerMatrixAttributes["initialEntropy"]:
					winnerMatrixAttributes = {
						"globalId":       result.globalId,
						"matrix":         result.matrix,
						"initialEntropy": result.initialEntropy
					}

			# xor winner with all peers, not itself as that would lose data
			for subSymbolGenerator in self.subSymbolGenerators:
				if subSymbolGenerator.globalId != winnerMatrixAttributes["globalId"]:
					subSymbolGenerator.matrix = xorMatrices(winnerMatrixAttributes["matrix"], subSymbolGenerator.matrix)
					subSymbolGenerator.finalEntropy = exputils.calcEntropy(subSymbolGenerator.matrix.flatten())["entropy"]
			
			# bundle matrices and replace own matrix
			newMatrices = []
			for subSymbolGenerator in self.subSymbolGenerators:
				newMatrices.append(subSymbolGenerator.matrix)
			if len(newMatrices) != 0:
				self.matrix = bundleMatrices(newMatrices)
				self.finalEntropy = exputils.calcEntropy(self.matrix.flatten())["entropy"]
			else:
				self.finalEntropy = self.initialEntropy
			
		return self
	
	def printSymbolGenerator(self, nestLevel = 0):
		print ("    " * nestLevel) + "Global ID:", self.globalId
		print ("    " * nestLevel) + "Level:", self.level
		print ("    " * nestLevel) + "Matrix Width:", self.matrixWidth
		print ("    " * nestLevel) + "Initial Entropy:", self.initialEntropy
		print ("    " * nestLevel) + "Final Entropy:", self.initialEntropy
		#print ("    " * nestLevel), self.matrix
		for x in xrange(0, len(self.subSymbolGenerators)):
			self.subSymbolGenerators[x].printSymbolGenerator(nestLevel = nestLevel + 1)
		
	
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
		raise ValueError("bundleMatrices expected 4 matrices, not " + str(matrixCount))
	topMatrices = numpy.concatenate((matrices[0], matrices[1]), axis = 1)
	bottomMatrices = numpy.concatenate((matrices[2], matrices[3]), axis = 1)
	outputMatrix = numpy.concatenate((topMatrices, bottomMatrices), axis = 0)
	return outputMatrix

def xorMatrices(leftMatrix, rightMatrix):
	length = len(leftMatrix)
	outputData = numpy.zeros(shape = (length, length), dtype = "uint8")
	for x in xrange(0, length):
		for y in xrange(0, length):
			if leftMatrix[x, y] != rightMatrix[x, y]:
				outputData[x, y] = 1

	return outputData
