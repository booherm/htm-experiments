import BitArray2D
import mutator
import os
import image_utils

os.system("clear")
print "Executing Matt's CA Experiment\n"

# Fredkin billiard ball model CA

iterationHashes = {}

inputMatrix = image_utils.getBitArray2DFromBitmapFile(filename = "alice_and_dodo.bmp", width = 512)
#inputMatrix = BitArray2D.BitArray2D(bitstring = "11111111\n10011011\n11010101\n10011011\n10101011\n10011011\n10001101\n11111111")
#inputMatrix = mutator.getRandomBitMatrix(width = 256)

# set border
for row in xrange(0, inputMatrix.rows):
	if row == 0 or row == inputMatrix.rows - 1:
		for col in xrange(0, inputMatrix.columns):
			inputMatrix[row, col] = 1
	else:
		inputMatrix[row, 0] = 1
		inputMatrix[row, inputMatrix.columns - 1] = 1

image_utils.writeBitArray2DImage(bitArray = inputMatrix, filename = "00000" + "__initial.png")
m = mutator.Mutator(matrix = inputMatrix, topLevelInstructions = None)
iterationHashes[m.getSha1Hash()] = True

for i in xrange(0, 10000):
	m.mutate(iteration = i)
	print "iteration", i, "complete"
	newHash = m.getSha1Hash()
	if newHash in iterationHashes:
		print "halting, cycle detected on iteration", i
		break;
	iterationHashes[m.getSha1Hash()] = True
