import json
from pathlib import Path
import LinkedList


def loadData(data,filePath):
    with open(filePath,'w') as scoreFile:
        json.dump(data,scoreFile)
    scoreFile.close()

def readData(filePath):
    with open(filePath,'r') as scoreFile:
        data = scoreFile.read()
    ans = json.loads(data)
    scoreFile.close()
    return ans

class MyListEncoder(json.JSONEncoder):
    def default(self,targetList):
        elements = targetList.readData()
        return {'__LinkedList__' : True, 'values' : elements}


    @staticmethod
    def as_LinkedList(encodedDict):
        if '__LinkedList__' in encodedDict:
            newList = LinkedList.LinkedList()
            valueArray = encodedDict['values']
            for element in valueArray:
                newList.insertInOrder(element[0],element[1])
            return newList


       


class ComplexEncoder(json.JSONEncoder):
    def default(self,z):
        if isinstance(z,complex):
            return {'__complex__' : True,'real' : z.real,'imag':z.imag}
        else:
            super().default(self,z)


filePath = str(Path.cwd() / "HighScores" / "complex.json")



z = 3 + 8j

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