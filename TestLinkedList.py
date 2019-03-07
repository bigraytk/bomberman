

import LinkedList
import unittest

class TestList(unittest.TestCase):

    def testList__init__(self):
        test = LinkedList.LinkedList()
        self.assertEqual(test.head,None)
        self.assertEqual(test.tail,None)
        self.assertEqual(test.numberOfNodes,0)

        flag = False
        try:
            test.head = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test.tail = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test.numberOfNodes = -1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test.numberOfNodes = 2.0
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testNode__init__(self):
        ll = LinkedList.LinkedList()
        num = 0
        name = 'jlw'
        testNode = ll.Node(num,name)
        self.assertEqual(testNode.nextNode,None)
        self.assertEqual(testNode.prevNode,None)
        self.assertEqual(testNode.score,0)
        self.assertEqual(testNode.name,'jlw')

        flag = False
        try:
            testNode.nextNode = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            testNode.prevNode = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            testNode.score = '1'
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            testNode.name = 1
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

    def testAppend(self):
        test = LinkedList.LinkedList()
        node1 = (1000,'jlw')
        node2 = (900, 'jjj')
        test.append(node1[0],node1[1])
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])
        test.append(node2[0],node2[1])
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node2[0])
        self.assertEqual(test.tail.name,node2[1])


        flag = False
        try:
            test.append('100','jlw')
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test.append(100,100)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)

        flag = False
        try:
            test.append(None,'jlw')
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)
        
        flag = False
        try:
            test.append(100,None)
        except RuntimeError as rte:
            flag = True
        finally:
            self.assertTrue(flag)


    def testReadTail(self):
        test = LinkedList.LinkedList()
        node1 = (1000,'jlw')
        node2 = (900, 'jjj')
        output = test.readTail()
        self.assertEqual(output,None)
        test.append(node1[0],node1[1])
        output = test.readTail()
        self.assertEqual(output[0],node1[0])
        self.assertEqual(output[1],node1[1])
        test.append(node2[0],node2[1])
        output = test.readTail()
        self.assertEqual(output[0],node2[0])
        self.assertEqual(output[1],node2[1])

    
    def testIndexOf(self):
        test = LinkedList.LinkedList()
        node1 = (1000,'jlw')
        node2 = (900, 'jjj')
        output = test.indexOf(1000,'jlw')
        self.assertEqual(output,None)
        test.append(node1[0],node1[1])
        output = test.indexOf(1000,'jlw')
        self.assertEqual(output,0)
        output = test.indexOf(1000,'jll')
        self.assertEqual(output,None)
        output = test.indexOf(100,'jlw')
        self.assertEqual(output,None)

        test.append(node2[0],node2[1])
        output = test.indexOf(900,'jjj')
        self.assertEqual(output,1)
        

    def testIndexOfSmallerScore(self):
        test = LinkedList.LinkedList()
        node1 = (1000,'jlw')
        node2 = (900, 'jjj')
        output = test.indexOfSmallerScore(100)
        self.assertEqual(output,None)
        test.append(node1[0],node1[1])
        output = test.indexOfSmallerScore(100)
        self.assertEqual(output,None)
        output = test.indexOfSmallerScore(1000)
        self.assertEqual(output,None)
        output = test.indexOfSmallerScore(1001)
        self.assertEqual(output,0)

        test.append(node2[0],node2[1])
        output = test.indexOfSmallerScore(100)
        self.assertEqual(output,None)
        output = test.indexOfSmallerScore(1000)
        self.assertEqual(output,1)
        output = test.indexOfSmallerScore(1001)
        self.assertEqual(output,0)

    def testInsertAtIndex(self):
        test = LinkedList.LinkedList()
        node1 = (1,'jlw')
        node2 = (2, 'jjj')
        node3 = (3, 'www')
        test.insertAtIndex(100,node1[0],node1[1])
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])

        test.insertAtIndex(100,node2[0],node2[1])
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node2[0])
        self.assertEqual(test.tail.name,node2[1])

        test.insertAtIndex(1,node3[0],node3[1])
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])

        output = test.indexOf(node3[0],node3[1])
        self.assertEqual(output,1)

        self.assertEqual(test.tail.score,node2[0])
        self.assertEqual(test.tail.name,node2[1])

    
    def testInsertInOrder(self):
        test = LinkedList.LinkedList()
        node1 = (1,'jlw')
        node2 = (2, 'jjj')
        node3 = (3, 'www')

        test.insertInOrder(node2[0],node2[1])
        self.assertEqual(test.head.score,node2[0])
        self.assertEqual(test.head.name,node2[1])
        self.assertEqual(test.tail.score,node2[0])
        self.assertEqual(test.tail.name,node2[1])

        test.insertInOrder(node1[0],node1[1])
        self.assertEqual(test.head.score,node2[0])
        self.assertEqual(test.head.name,node2[1])
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])

        test.insertInOrder(node3[0],node3[1])
        self.assertEqual(test.head.score,node3[0])
        self.assertEqual(test.head.name,node3[1])
        output = test.indexOf(node2[0],node2[1])
        self.assertEqual(output,1)
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])



    def testDeleteAtIndex(self):
        test = LinkedList.LinkedList()
        node1 = (1,'jlw')
        node2 = (2, 'jjj')
        node3 = (3, 'www')
        test.append(node1[0],node1[1])
        test.deleteAtIndex(100)
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])
        test.append(node2[0],node2[1])
        test.append(node3[0],node3[1])

        test.deleteAtIndex(0)
        self.assertEqual(test.head.score,node2[0])
        self.assertEqual(test.head.name,node2[1])
        self.assertEqual(test.tail.score,node3[0])
        self.assertEqual(test.tail.name,node3[1])

        test.deleteAtIndex(1)
        self.assertEqual(test.head.score,node2[0])
        self.assertEqual(test.head.name,node2[1])
        self.assertEqual(test.tail.score,node2[0])
        self.assertEqual(test.tail.name,node2[1])


    def testDeleteTail(self):
        test = LinkedList.LinkedList()
        node1 = (1,'jlw')
        node2 = (2, 'jjj')
        node3 = (3, 'www')
        test.deleteTail()
        self.assertEqual(test.head,None)
        self.assertEqual(test.tail,None)

        test.append(node1[0],node1[1])
        test.deleteTail()
        self.assertEqual(test.head,None)
        self.assertEqual(test.tail,None)

        test.append(node1[0],node1[1])
        test.append(node2[0],node2[1])
        test.deleteTail()
        self.assertEqual(test.head.score,node1[0])
        self.assertEqual(test.head.name,node1[1])
        self.assertEqual(test.tail.score,node1[0])
        self.assertEqual(test.tail.name,node1[1])

    def testEmpty(self):
        test = LinkedList.LinkedList()
        node1 = (1,'jlw')
        output = test.empty()
        self.assertEqual(output,True)

        test.append(node1[0],node1[1])
        output = test.empty()
        self.assertEqual(output,False)

    def testReadData(self):
        test = LinkedList.LinkedList()
        node1 = (1000,'jlw')
        node2 = (900, 'jjj')
        test.append(node1[0],node1[1])
        test.append(node2[0],node2[1])
        output = test.readData()
        self.assertEqual(output[0][0],node1[0])
        self.assertEqual(output[0][1],node1[1])
        self.assertEqual(output[1][0],node2[0])
        self.assertEqual(output[1][1],node2[1])


    '''
    Not providing unit test for the str methods, as those are never called by the program. 
    They were only made for troubleshooting purposes to be used when creating the methods.
    '''





if __name__ == "__main__":
    unittest.main(exit=False)