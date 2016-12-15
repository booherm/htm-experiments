import BitArray2D
import mutator
import os
import image_utils

os.system("clear")
print "Executing Matt's HTM Experiment\n"

for i in xrange(0, 10000):
	inputMatrix = mutator.getRandomBitMatrix(width = 256)
	image_utils.writeBitArray2DImage(bitArray = inputMatrix, filename = "img_" + str(i).zfill(5) + ".png")
	print "iteration", i, "complete"
