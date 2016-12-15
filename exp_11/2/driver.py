import BitArray2D
import mutator
import os
import image_utils

os.system("clear")
print "Executing Matt's GI Experiment\n"

iterationHashes = {}

#inputMatrix = image_utils.getBitArray2DFromBitmapFile(filename = "alice_and_dodo.bmp", width = 512)
#inputMatrix = BitArray2D.BitArray2D(bitstring = "11111111\n10011011\n11010101\n10011011\n10101011\n10011011\n10001101\n11111111")
inputMatrix = mutator.getRandomBitMatrix(width = 256)

image_utils.writeBitArray2DImage(bitArray = inputMatrix, filename = "00000" + "__initial.png")
m = mutator.Mutator(matrix = inputMatrix, topLevelInstructions = None)
iterationHashes[m.getSha1Hash()] = True

for i in xrange(0, 200):
	m.mutate(iteration = i)
	print "iteration", i, "complete"
	newHash = m.getSha1Hash()
	if newHash in iterationHashes:
		print "halting, cycle detected on iteration", i
		break;
	iterationHashes[m.getSha1Hash()] = True
