#class Transaction incapsulates representation of transaction provided
#by bitcoind, so that we don't depend on it
class Transaction(object):
    def __init__(self, tx):
        self.set(tx)
        
    #we are going to parse only what we need, if we will need more, we will add
    #more parsing
    def set(self, tx):
        self.id = tx['txid']
        self.inputs = list()
        for i in tx['vin']:
            if 'coinbase' in i:
                self.inputs.append({'txid':i['coinbase'], 'outindx':0})
            else:
                self.inputs.append({'txid':i['txid'], 'outindx':i['vout']})
        self.outputs = list()
        for i in tx['vout']:
            self.outputs.append(i['value'])
            
        
class ColoredOutput(object):
    def __init__(self, value, label):
        self.value = value
        self.label = label


class ColoredSeed(object):
    def __init__(self, txhash, outputs, color_id):
        self.txhash = txhash
        self.outputs = outputs
        self.color_id = color_id