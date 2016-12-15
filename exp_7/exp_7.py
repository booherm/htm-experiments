import BitArray2D
import mutator
import os
import image_utils

os.system("clear")
print "Executing Matt's HTM Experiment\n"

#ba = BitArray2D.BitArray2D(bitstring = "11111111\n00000000\n01010101")
#print ba
#print "---------------"
#
#ba[1, 1] = 1
#print ba
#print "---------------"
#
#someBit = ba[BitArray2D.godel(0, 0)]
#print "someBit =", someBit
#print "---------------"
#
#subArray = ba[BitArray2D.godel(0, 0) : BitArray2D.godel(2, 2)]
#print subArray
#print "---------------"
#
#ba[1, 1] = 0
#print subArray
#

#inputMatrix = BitArray2D.BitArray2D(bitstring = "1111\n0000\n1010\n0101")

inputMatrix = image_utils.getBitArray2DFromBitmapFile(filename = "alice_and_dodo.bmp", width = 512)
mutator.writeMatrixImage(matrix = inputMatrix, filename = "test_00000.png")
m = mutator.Mutator(matrix = inputMatrix)

for i in xrange(0, 100):
	finalInstructions = m.mutate()
	print "iteration", i, "complete"
	m.printOperationStats()
	mutator.writeMatrixImage(matrix = inputMatrix, filename = "test_" + str(i + 1).zfill(5) + ".png")
