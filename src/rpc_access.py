from bitcoinrpc import authproxy
import json

def create(host, uname, pwd, port, ssl):
    fullUrl= 'http'
    if ssl == True:
        fullUrl += 's'
    fullUrl += '://'
    fullUrl += uname
    fullUrl += ':'
    fullUrl += pwd
    fullUrl += '@'
    fullUrl += host
    fullUrl += ':'
    if len(str(port)) > 0:
        fullUrl += str(port)
    access =  authproxy.AuthServiceProxy(fullUrl)
    return access

def fromFile(fileName):
    f = open(fileName)
    parsedData = json.load(f)
    return create(parsedData['host'], parsedData['uname'], parsedData['pwd'],
                  parsedData['port'], parsedData['ssl'])