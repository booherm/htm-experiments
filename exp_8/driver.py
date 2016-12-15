import BitArray2D
import mutator
import os

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

#  00 00 00 00
#  00 01 10 11
#  
#  01 01 01 01
#  00 01 10 11
#  
#  10 10 10 10
#  00 01 10 11
#  
#  11 11 11 11
#  00 01 10 11

# send top level entropy down the chain.  

inputMatrix = BitArray2D.BitArray2D(bitstring = "00000000\n00011011\n01010101\n00011011\n10101010\n00011011\n11111111\n00011011")
#inputMatrix = mutator.getRandomBitMatrix(8)
mutator.writeMatrixImage(matrix = inputMatrix, filename = "test_00000.png")
m = mutator.Mutator(matrix = inputMatrix)

for i in xrange(0, 100):
	finalInstructions = m.mutate()
	print "iteration", i, "complete"
	m.printOperationStats()
	mutator.writeMatrixImage(matrix = inputMatrix, filename = "test_" + str(i + 1).zfill(5) + ".png")
