import BitArray2D
import mutator
import os
import image_utils

os.system("clear")
print "Executing Matt's HTM Experiment\n"

# initial top instruction = [0101]
# Going down, calc total entropy of all quadrants.  If > entropyTarget, dec, else inc.  Pass inc/dec down.
# At bottom, current boolean operator if call is to dec, ?? if call is to inc.
#	If inc and desired output inc, apply nand, return 1.
#	else if dec and desired output dec, apply nand, return 1.
#   return 0 // nand would not take entropy in desired direction, do nothing
# back from recursive call, each quad returned a 0 or 1, result = [0010]
#   nand with top instruction.
#	If inc and desired output inc, apply nand, return 1.
#	else if dec and desired output dec, apply nand, return 1.
#   return 0 // nand would not take entropy in desired direction, do nothing
# if top layer, top instcution = result
# inc/dec constant going down, along with top instruction


iterationHashes = {}

#inputMatrix = image_utils.getBitArray2DFromBitmapFile(filename = "alice_and_dodo.bmp", width = 512)
inputMatrix = BitArray2D.BitArray2D(bitstring = "00000000\n00011011\n01010101\n00011011\n10101010\n00011011\n11111111\n00011011")
mutator.writeMatrixImage(matrix = inputMatrix, filename = "test_00000.png")
m = mutator.Mutator(matrix = inputMatrix, topLevelInstructions = "0101", targetEntropy = 0.5)
iterationHashes[m.getSha1Hash()] = True

for i in xrange(0, 3):
	m.mutate()
	print "iteration", i, "complete"
	mutator.writeMatrixImage(matrix = m.matrix, filename = "test_" + str(i + 1).zfill(5) + ".png")
	
	newHash = m.getSha1Hash()
	if newHash in iterationHashes:
		print "halting, cycle detected on iteration", i
		break;
	iterationHashes[m.getSha1Hash()] = True

