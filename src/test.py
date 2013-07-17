from build import ColorBuilder
from transaction import *
from ordercoloring import orderColoring
from storage import Storage


txhashes = ['b1586cd10b32f78795b86e9a3febe58dcb59189175fad884a7f4a6623b77486e',
            '8f6c8751f39357cd42af97a67301127d497597ae699ad0670b4f649bd9e39abf']

def simplePrint(x):
    print(x)

def silent(x):
    pass

blueColorId = 1
blueSeed = ColoredSeed(txhashes[0], [ColoredOutput(1, ''),], blueColorId)
builder = ColorBuilder(blueSeed, orderColoring, simplePrint)
builder.build()

stor = Storage()
with stor:
    res = stor.get_all(blueColorId)
for i in res:
    print(i)