import rpc_access
from storage import Storage
from transaction import Transaction

class ColorBuilder(object):
    def __init__(self, seed, kernel, printer):
        self.__seed = seed
        self.__kernel = kernel
        self.__storage = Storage()
        self.__knownTxs = set((seed.txhash,))
        self.__access = rpc_access.fromFile('../data/rpc.ini')
        self.__printer = printer
        coloredTxs = self.__storage.get_all(seed.color_id)
        for tx in coloredTxs:
            self.__knownTxs.add(str(tx[0]))
            
    def isColored(self, tx):
        for inp in tx.inputs:
            if ('txid' in inp) and (inp['txid'] in self.__knownTxs):
                return True
        return False

    def processBlock(self, blockHeight):
        txhashes = self.__access.getblock(self.__access.getblockhash(blockHeight))['tx']
        for txhash in txhashes:
            tx = Transaction(self.__access.getrawtransaction(txhash, 1))
            if not self.isColored(tx):
                continue
            
            colorVals = list()
            self.__printer(txhash + ", inputs: " + str(len(tx.inputs)) + ", outputs: " + str(len(tx.outputs)))

            for inp in tx.inputs:
                prevHash = inp['txid']
                prevTx = Transaction(self.__access.getrawtransaction(prevHash, 1))
#                   print(str(t1.duration_in_seconds())  + ", inputs: " + str(len(prevTx['vin'])) + ", outputs: " + str(len(prevTx['vout'])))
                prevOutIndex = inp['outindx']
                colorVal = self.__storage.get(self.__seed.color_id, prevHash, prevOutIndex)
                colorVals.append((prevTx.outputs[prevOutIndex], colorVal))
            colorOuts = self.__kernel(tx, colorVals)

            colorFound = False
            for i, colorOut in enumerate(colorOuts):
                if colorOut[0] != 0:
                    self.__storage.add(self.__seed.color_id, txhash, i, colorOut[0], colorOut[1])
                    colorFound = True
            if colorFound:
                self.__knownTxs.add(str(txhash))
                

    def build(self):
        seedTransaction = self.__access.getrawtransaction(self.__seed.txhash, 1)
        for i, seedOut in enumerate(self.__seed.outputs):
            self.__storage.add(self.__seed.color_id, self.__seed.txhash, i, seedOut.value, seedOut.label)
            
        block = self.__access.getblock(seedTransaction['blockhash'])
        blockHeight = block['height']
        while blockHeight <= self.__access.getblockcount():
            self.__printer(blockHeight)
            self.processBlock(blockHeight)
            blockHeight += 1
