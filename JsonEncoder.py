import json
from pathlib import Path
import LinkedList


def loadData(data,filePath):
    '''Global function that saves data as a .json file'''

    if not isinstance(data,LinkedList.LinkedList):
        raise RuntimeError('Error: data must be an instance of LinkedList')


    try:
        with open(filePath,'w') as scoreFile:
            json.dump(data,scoreFile, cls = MyListEncoder)
        scoreFile.close()
    except:
        raise RuntimeError('Error: unable to open ' , filePath , ' or execute json.dump')

def readData(filePath):
    '''Global function that decodes a .json file, and runs it through custom decoder. Only use for LinkedList objects'''
    try:
        with open(filePath,'r') as scoreFile:
            data = scoreFile.read()
        unpacked = json.loads(data)
        scoreFile.close()
    except:
        raise RuntimeError('Error: unable to open ' , filePath , ' or execute json.loads')

    newList = MyListEncoder.as_LinkedList(unpacked)
    
    return newList

class MyListEncoder(json.JSONEncoder):
    '''Custom Encoder that enables encoding of LinkedList object'''
    def default(self,targetList):
        elements = targetList.readData()
        return {'__LinkedList__' : True, 'values' : elements}


    @staticmethod
    def as_LinkedList(encodedDict):
        '''Custom Decoder that enables decode/creation of LinkedList object'''
        if '__LinkedList__' in encodedDict:
            newList = LinkedList.LinkedList()
            valueArray = encodedDict['values']
            for element in valueArray:
                newList.insertInOrder(element[0],element[1])
            return newList


       


if __name__=="__main__":

    data = LinkedList.LinkedList()
    data.append(100,'jlw')
    data.append(200,'aaa')


    test = json.dumps(data,cls=MyListEncoder)
    print(test)

    unpacked = json.loads(test)
    newList = MyListEncoder.as_LinkedList(unpacked)
    print(newList)
    newList.insertInOrder(50,'bbb')
    print(newList)

    '''
    loadData(data,filePath)


    #test = readData(filePath)
    #print(test)


    '''