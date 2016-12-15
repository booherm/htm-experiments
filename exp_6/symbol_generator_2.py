import exputils
import math
import numpy

class _Quadrant:
	def __init__(self, quadrantWidth, topCoordinate, leftCoordinate):
		self.quadrantWidth = quadrantWidth
		self.topCoordinate = topCoordinate
		self.leftCoordinate = leftCoordinate

class SymbolGenerator:

	initialEntropy = None
	finalEntropy = None
	matrix = None
	_imageFileNamePrefix = None
	_matrixWidth = None
	_maxIterations = None
	_imageFrame = None
	_movieFilename = None
		
	def generateSymbol(self, matrix, maxIterations = 20, movieFilename = None):
		self.matrix = matrix[:]
		self._matrixWidth = len(self.matrix)
		mainQuadrant = _Quadrant(quadrantWidth = self._matrixWidth, leftCoordinate = 0, topCoordinate = 0)
		self.initialEntropy = self.__calcEntropy(mainQuadrant)
		self._maxIterations = maxIterations
		self._imageFrame = 0
		self._movieFilename = movieFilename
		
		if self._movieFilename is not None:
			self._imageFileNamePrefix = self._movieFilename
			exputils.writeMatrixImage(matrix = self.matrix, filename = self._imageFileNamePrefix + str(self._imageFrame).zfill(5) + ".png")
			self._imageFrame = self._imageFrame + 1
		
		self.finalEntropy = self.__process(quadrant = mainQuadrant)
		
		if self._movieFilename is not None:
			exputils.generateMovie(pngFilenamePattern = self._imageFileNamePrefix + "*.png", outputFilename = self._movieFilename, fps = 5)

	def __process(self, quadrant):
		previousEntropy = self.initialEntropy
		iterationExecutions = 0
		for i in xrange(0, self._maxIterations):
			print "main loop iteration", iterationExecutions
			newEntropy = self.__recursiveStep(level = 0, quadrant = quadrant)
			
			if self._movieFilename is not None:
				exputils.writeMatrixImage(matrix = self.matrix, filename = self._imageFileNamePrefix + str(self._imageFrame).zfill(5) + ".png")
				self._imageFrame = self._imageFrame + 1

			iterationExecutions = iterationExecutions + 1
			if previousEntropy == newEntropy:
				break
			previousEntropy = newEntropy
			
		return newEntropy
		
	def __recursiveStep(self, level, quadrant):
		if quadrant.quadrantWidth == 2:
			stepInitialEntropy = self.__calcEntropy(quadrant)
			print "start recursive step, level =", level, "quadrant =", quadrant.topCoordinate, quadrant.leftCoordinate, quadrant.quadrantWidth, "stepInitialEntropy =", stepInitialEntropy
			print " stop recursive step, level =", level, "quadrant =", quadrant.topCoordinate, quadrant.leftCoordinate, quadrant.quadrantWidth, "return entropy  =", stepInitialEntropy
			return stepInitialEntropy
		elif quadrant.quadrantWidth > 1:
			
			stepInitialEntropy = self.__calcEntropy(quadrant)
			print "start recursive step, level =", level, "quadrant =", quadrant.topCoordinate, quadrant.leftCoordinate, quadrant.quadrantWidth, "stepInitialEntropy =", stepInitialEntropy
			
			# determine sub-quadrants
			subQuadrants = []
			subQuadrantWidth = quadrant.quadrantWidth / 2
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = 0, leftCoordinate = 0))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = 0, leftCoordinate = subQuadrantWidth))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = subQuadrantWidth, leftCoordinate = 0))
			subQuadrants.append(_Quadrant(quadrantWidth = subQuadrantWidth, topCoordinate = subQuadrantWidth, leftCoordinate = subQuadrantWidth))

			for subQuadrant in subQuadrants:
				subQuadrant.entropy = self.__process(subQuadrant)

			# determine sub-quadrant with lowest entropy
			minEntropy = None
			winnerSubQuadrant = None
			for subQuadrant in subQuadrants:
				entropy = subQuadrant.entropy
				if minEntropy is None or entropy < minEntropy:
					minEntropy = entropy
					winnerSubQuadrant = subQuadrant
					
			# xor winner sub-quadrant with all sub-quadrants
			#print "winnerSubQuadrant topCoordinate =", winnerSubQuadrant.topCoordinate, "leftCoordinate =", winnerSubQuadrant.leftCoordinate
			#print "matrix before winner xor"
			#print self.matrix
			# we have to xor the winner quadrant with itself last
			xorQuadrants = []
			for subQuadrant in subQuadrants:
				if subQuadrant != winnerSubQuadrant:
					xorQuadrants.append(subQuadrant)
					#print "pushing subquadrant at:", subQuadrant.topCoordinate, subQuadrant.leftCoordinate
			xorQuadrants.append(winnerSubQuadrant)
			#print "pushing winner subquadrant at:", winnerSubQuadrant.topCoordinate, winnerSubQuadrant.leftCoordinate
			for subQuadrant in xorQuadrants:
				#print " "
				for row in xrange(0, subQuadrantWidth):
					for column in xrange(0, subQuadrantWidth):
						value = False
						winnerTopCoordinate = winnerSubQuadrant.topCoordinate + row
						winnerLeftCoordinate = winnerSubQuadrant.leftCoordinate + column
						peerTopCoordinate = subQuadrant.topCoordinate + row
						peerLeftCoordinate = subQuadrant.leftCoordinate + column
						#print "    winner coordinate =", winnerTopCoordinate, winnerLeftCoordinate
						#print "    peer coordinate   =", peerTopCoordinate, peerLeftCoordinate

						if self.matrix[peerTopCoordinate, peerLeftCoordinate] != self.matrix[winnerTopCoordinate, winnerLeftCoordinate]:
							value = True
						self.matrix[peerTopCoordinate, peerLeftCoordinate] = value
						#print "    set value at row", peerTopCoordinate, "column", peerLeftCoordinate, "to", value
			#print "matrix after winner xor"
			#print self.matrix
			
			#newEntropy = self.__calcEntropy(quadrant)
			#print " stop recursive step, level =", level, "quadrant =", quadrant.topCoordinate, quadrant.leftCoordinate, quadrant.quadrantWidth, "return entropy  =", newEntropy

			newEntropy = stepInitialEntropy
			print " stop recursive step, level =", level, "quadrant =", quadrant.topCoordinate, quadrant.leftCoordinate, quadrant.quadrantWidth, "return entropy  =", newEntropy
			return newEntropy

	def __calcEntropy(self, quadrant):
		totalCount = quadrant.quadrantWidth * quadrant.quadrantWidth
		trueCount = 0
		for y in xrange(quadrant.topCoordinate, quadrant.topCoordinate + quadrant.quadrantWidth):
			for x in xrange(quadrant.leftCoordinate, quadrant.leftCoordinate + quadrant.quadrantWidth):
				if self.matrix[y, x]:
					trueCount = trueCount + 1
		falseCount = totalCount - trueCount
	
		pctFalse = float(falseCount) / totalCount
		pctTrue = float(trueCount) / totalCount
		if pctFalse == 1 or pctTrue == 1:
			entropy = 0
		else:
			entropy = -((math.log(pctFalse, 2) * pctFalse) + (math.log(pctTrue, 2) * pctTrue))
		
		return entropy

