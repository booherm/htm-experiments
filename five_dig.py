import exputils

def xor(left, right):
	result = ""
	for x in xrange(0, len(left)):
		if left[x] != right[x]:
			result += "1"
		else:
			result += "0"
	return result
	
digits = 4
operands = []
for x in xrange(0, 2 ** digits):
	operands.append("{0:b}".format(x).zfill(digits))
	
for lop in operands:
	for rop in operands:
		xored = xor(lop, rop)
		lopPatternArray = map(int, list(lop))
		ropPatternArray = map(int, list(rop))
		xoredPatternArray = map(int, list(xored))
		
		lopEntropy = exputils.calcEntropy(lopPatternArray)["entropy"]
		ropEntropy = exputils.calcEntropy(ropPatternArray)["entropy"]
		xoredEntropy = exputils.calcEntropy(xoredPatternArray)["entropy"]
		
		change = "same"
		if(xoredEntropy < lopEntropy):
			change = "dec"
		elif(xoredEntropy > lopEntropy):
			change = "inc"
		
		print "\"" + lop + "_" + rop + "\": \"" + change + "\","
		#print lop, lopEntropy, rop, ropEntropy, xored, xoredEntropy, change

#for x in xrange(0, len(fiveDigits)):
#	print exputils.calcEntropy(fiveDigits[x])["entropy"]