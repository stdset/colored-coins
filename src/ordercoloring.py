import decimal

def isColored(colorVal):
    return bool(colorVal[1]) and (colorVal[1][0] != 0)

def orderColoring(tx, colorVals):
    res = list()
    inpIndex = 0
    zero = decimal.Decimal('0.0')
    suppliedValue = zero
    for out in tx.outputs:
        colorGood = True
        if suppliedValue > zero:
            colorGood = isColored(colorVals[max(inpIndex - 1, 0)])
        while suppliedValue < out:
            suppliedValue += colorVals[inpIndex][0]
            if not isColored(colorVals[inpIndex]):
                colorGood = False
            inpIndex += 1
        res.append((int(colorGood), ''))
        suppliedValue -= out
    return res
