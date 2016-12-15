import exputils

def performBitArrayOperations(leftArray, rightArray):
	left = ""
	right = ""
	andResult = ""
	andResultArray = []
	orResult = ""
	orResultArray = []
	xorResult = ""
	xorResultArray = []
	nandResult = ""
	nandResultArray = []
	
	for x in xrange(0, len(leftArray)):
		left += str(leftArray[x])
		right += str(rightArray[x])
		
		if leftArray[x] == rightArray[x] and leftArray[x] == 1:
			andResult += "1"
			andResultArray.append(1)
		else:
			andResult += "0"
			andResultArray.append(0)
		
		if leftArray[x] == 1 or rightArray[x] == 1:
			orResult += "1"
			orResultArray.append(1)
		else:
			orResult += "0"
			orResultArray.append(0)
		
		if leftArray[x] == rightArray[x]:
			xorResult += "0"
			xorResultArray.append(0)
		else:
			xorResult += "1"
			xorResultArray.append(1)
			
		if leftArray[x] == rightArray[x] and leftArray[x] == 1:
			nandResult += "0"
			nandResultArray.append(0)
		else:
			nandResult += "1"
			nandResultArray.append(1)

	print(left, exputils.calcEntropy(leftArray)["entropy"],
		right, exputils.calcEntropy(rightArray)["entropy"],
		andResult, exputils.calcEntropy(andResultArray)["entropy"],
		orResult, exputils.calcEntropy(orResultArray)["entropy"],
		xorResult, exputils.calcEntropy(xorResultArray)["entropy"],
		nandResult, exputils.calcEntropy(nandResultArray)["entropy"]
	)

	
			
leftOperands = []
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 0])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 0, 1])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 0])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 0, 1, 1])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 0])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 0, 1])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 0])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([0, 1, 1, 1])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 0])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 0, 1])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 0])
leftOperands.append([1, 0, 1, 1])
leftOperands.append([1, 0, 1, 1])
leftOperands.append([1, 0, 1, 1])
leftOperands.append([1, 0, 1, 1])
leftOperands.append([1, 0, 1, 1])
leftOperands.append([1, 1, 0, 0])
leftOperands.append([1, 1, 0, 0])
leftOperands.append([1, 1, 0, 0])
leftOperands.append([1, 1, 0, 0])
leftOperands.append([1, 1, 0, 1])
leftOperands.append([1, 1, 0, 1])
leftOperands.append([1, 1, 0, 1])
leftOperands.append([1, 1, 1, 0])
leftOperands.append([1, 1, 1, 0])
leftOperands.append([1, 1, 1, 1])

rightOperands = []
rightOperands.append([0, 0, 0, 0])
rightOperands.append([0, 0, 0, 1])
rightOperands.append([0, 0, 1, 0])
rightOperands.append([0, 0, 1, 1])
rightOperands.append([0, 1, 0, 0])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 0, 0, 1])
rightOperands.append([0, 0, 1, 0])
rightOperands.append([0, 0, 1, 1])
rightOperands.append([0, 1, 0, 0])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 0, 1, 0])
rightOperands.append([0, 0, 1, 1])
rightOperands.append([0, 1, 0, 0])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 0, 1, 1])
rightOperands.append([0, 1, 0, 0])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 1, 0, 0])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 1, 0, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 1, 1, 0])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([0, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 0, 0, 0])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 0, 0, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 0, 1, 0])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 0, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 1, 0, 0])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 1, 0, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 1, 1, 0])
rightOperands.append([1, 1, 1, 1])
rightOperands.append([1, 1, 1, 1])

for x in xrange(0, len(leftOperands)):
	performBitArrayOperations(leftOperands[x], rightOperands[x])
		