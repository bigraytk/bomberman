import pickle
from pathlib import Path
import sys
import JsonEncoder
import json


class LinkedList(object):
    
    '''Linked-List Class.
    '''
    class Node(object):
        '''Node Class

        This is an internally defined class, indicating it is not a thing to be
        used willy-nilly elsewhere in the code.

        '''
        def __init__(self, score, name):
            ''' Constructor. score must be an int, name must be a str'''
            
            self.score = score
            self.name = name
            self.nextNode = None    
            self.prevNode = None
        
        @property
        def score(self):
            return self.__score

        @property
        def name(self):
            return self.__name

        @property
        def nextNode(self):
            ''' Accessor. '''
            return self.__nextNode

        @property
        def prevNode(self):
            ''' Accessor. '''
            return self.__prevNode

        @score.setter
        def score(self,nextIn):
            if not isinstance(nextIn,int):
                raise RuntimeError('Error: The value for score must be an int')
            self.__score = nextIn

        @name.setter
        def name(self,nextIn):
            if not isinstance(nextIn,str):
                raise RuntimeError('Error: The value for name must be a string')
            self.__name = nextIn

        @nextNode.setter
        def nextNode(self, nextIn):
            '''Sets the next node. Allows None indicating the end of the List,
            but no other non-Node assignment '''
            
            if nextIn and not isinstance(nextIn, self.__class__):
                raise RuntimeError(str(nextIn) + ' is not a linked-list Node.')
            self.__nextNode = nextIn

        @prevNode.setter
        def prevNode(self, nextIn):
            '''Sets the previous node. Allows None indicating the end of the List,
            but no other non-Node assignment '''
            
            if nextIn and not isinstance(nextIn, self.__class__):
                raise RuntimeError(str(nextIn) + ' is not a linked-list Node.')
            self.__prevNode = nextIn

        def __str__(self):
            if self.prevNode == None:
                p = False
            else:
                p = True
            if self.nextNode == None:
                n = False
            else:
                n = True
            return str(self.score) + ':' + str(self.name) + ' prevNode = ' + str(p) + ' nextNode = ' + str(n)

        #end of inner-class Node
        ####################################


    def __init__(self):
        ''' Constructor. Allocates an empty Linked-List shell. '''
        print('in the constructor')
        self.head = None
        self.tail = None
        self.numberOfNodes = 0

    @property
    def head(self):
        return self.__head

    @property
    def tail(self):
        return self.__tail

    @property
    def numberOfNodes(self):
        return self.__numberOfNodes

    @numberOfNodes.setter
    def numberOfNodes(self,value):
        if value < 0 or not isinstance(value,int):
            raise RuntimeError('Error: numberOfNodes but be and integer greater than or equal to 0')
        self.__numberOfNodes = value

    @tail.setter
    def tail(self,value):
        node = self.Node(0,'test')
        if value!= None and not isinstance(value,node.__class__):
            raise RuntimeError('Error: Head must point to None or a Node')
        self.__tail = value

    @head.setter
    def head(self,value):
        node = self.Node(0,'test')
        if value!= None and not isinstance(value,node.__class__):
            raise RuntimeError('Error: Head must point to None or a Node')
        self.__head = value

    def readData(self):
        ''' Returns all the data in the nodes as a list. '''
        if self.head:
            answer = []
            current = self.head
            while current:
                data = (current.score,current.name)
                answer.append(data)
                current = current.nextNode
        else:
            answer = []   
        return answer

    def readTail(self):
        '''Returns the score and name of the tail in a tuple (score,name)'''
        if self.tail:
            return (self.tail.score,self.tail.name)
        else:
            return None

   
    def indexOf(self, value, name):
        '''Returns index of first matching value, or None if value not found.'''
        
        if self.head:
            current = self.head
            i = 0
            while not current.score == value and not current.name == name and current.nextNode:
                current = current.nextNode
                i += 1

            if current.score == value and current.name == name:
                answer = i
            else:
                answer = None
        else:
            answer = None
            
        return answer

    def indexOfSmallerScore(self, value):
        '''Returns index of the first score that is smaller than value, or None if value not found.'''
        
        if self.head:
            current = self.head
            i = 0
            while not current.score < value and current.nextNode:
                current = current.nextNode
                i += 1

            if current.score < value:
                answer = i
            else:
                answer = None
        else:
            answer = None
            
        return answer

    
    def append(self, score, name):
        '''Appends new data Node to the end of the list. '''
        self.numberOfNodes += 1   
        newNode = self.Node(score,name)
        if self.tail == None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.nextNode = newNode
            newNode.prevNode = self.tail
            self.tail = newNode
            

    def insertAtIndex(self, index, score, name):
        '''Inserts new Node at index, appends to end if index beyond end. '''
        self.numberOfNodes += 1

        newNode = self.Node(score,name)
        #print('insterting new node: ' , newNode)
        if self.head:
            if index == 0:
                newNode.nextNode = self.head
                self.head.prevNode = newNode
                self.head = newNode
            else:
                current = self.head
                i = 0
                while i < index-1 and current.nextNode:
                    current = current.nextNode
                    i += 1

                #print('current: ' , current)
                
                if i == index-1:
                    newNode.nextNode = current.nextNode
                    current.nextNode.prevNode = newNode
                    newNode.prevNode = current
                    current.nextNode = newNode
                else:
                    current.nextNode = newNode
                    newNode.prevNode = current
                    self.tail = newNode
        else:
            self.head = newNode
            self.tail = newNode


    def insertInOrder(self, score, name):
        '''Inserts new Node in order, highest score at the head, lowest at the tail '''
        index = self.indexOfSmallerScore(score)
        if index == None:
            self.append(score,name)
        else:
            self.insertAtIndex(index,score,name)

      


    def deleteAtIndex(self, index):
        '''Deletes Node at index, silent completion, no error generated if
        index beyond end of list. '''

        if self.head == None:
            return

        if index == 0:
            self.head = self.head.nextNode
            self.head.prevNode = None
            self.numberOfNodes -= 1
        else:
            current = self.head
            i = 0
            while i < index and current.nextNode:
                current = current.nextNode
                i += 1

            if i == index and current.nextNode:
                #print('current: ' ,current)
                current.nextNode = current.nextNode.nextNode
                self.numberOfNodes -= 1
            elif i == index and not current.nextNode:
                current.prevNode.nextNode = None
                self.tail = current.prevNode
                self.numberOfNodes -= 1

    def deleteTail(self):
        '''Deletes the tail Node, if tail and head are same Node, will delete both. No return'''
        if self.tail == self.head:
            self.head = None
            self.tail = None
            self.numberOfNodes = 0
        else:
            #print('deleting: ' , self.tail)
            self.tail = self.tail.prevNode
            #print('new tail is : ' , self.tail)
            self.tail.nextNode = None
            self.numberOfNodes -= 1
        


    def empty(self):
        '''Returns True if the List is empty, False otherwise.'''
        if self.head:
            return False
        else:
            return True  




    def __str__(self):

        if self.head == None:
            return ''
        
        current = self.head
        result = str(current.score) + ':' + str(current.name)

        while current.nextNode:
            current = current.nextNode
            result += ', ' + str(current.score) + ':' + str(current.name)      

        return result







##########################################################
#testing-related

def saveBlankList():
    scoreList = LinkedList()
    scoreList.append(1000,'JLW')
    filePath = str(Path.cwd() / "HighScores" / "Scores.json")
    JsonEncoder.loadData(scoreList,filePath)
    
##########################################################
#main


if __name__=="__main__":
    saveBlankList()

    '''
    filePath = str(Path.cwd() / "HighScores" / "Scores.pickle")
    test = loadList(filePath)
    print(test)
    array = test.readData()
    print(array)
    print(test.numberOfNodes)
    
    

    
    test.append(400,'bAA')
    print(test)
    saveList(test,filePath)
    '''
    

    
    
