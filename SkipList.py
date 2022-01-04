import random
import time

#Nodes are initialized inside of the skiplist, but need to be constructed with the # of levels to be used and their data. 
class Node:
    def __init__(self, levels, data):
        self.data = data
        self.nextPointers = [None] * levels
        self.prevPointers = [None] * levels
        
    def __str__(self):
        return str(self.data)

class SkipList:
    def __init__(self, levels):
        self.heads = [None] * levels
        self.levels = levels
        self.count = 0

    #inserts the node at the correct sorted location in the linked list.
    #Then, for every successful coin flip, inserts it at the correct sorted location in the linked list above.
    def insert(self, data):
        newNode = Node(self.levels, data)
        self.insertIntoLevel(0,newNode)
        self.count+=1
        currLevel = 1
        choice = random.choice(range(0,100))
        while currLevel < self.levels:
            if  choice < 50:
                break
            else:
                self.insertIntoLevel(currLevel, newNode)
                currLevel = currLevel + 1
                choice = random.choice(range(0,100))

    #Returns the first node with matching data found, or None if one does not exist. 
    def findNode(self,data):
        currLevel = self.levels-1

        #find the first nonempty level
        while self.heads[currLevel] == None:
            currLevel = currLevel - 1

        #start the search at the first head of the highest non-empty level.
        currNode = self.heads[currLevel]

        #While we're not on the lowest level
        while currLevel > 0:
            #if the head of this level is bigger than the node we're looking for, move down a level.
            if self.heads[currLevel].data > data:
                currLevel = currLevel - 1
                currNode = self.heads[currLevel]
                continue
            #the current node becomes the first node less than or equal to data at the current level. Start searching at
            #currNode.
            currNode = self.findFirstNodeLessThanOrEqualTo(currNode,currLevel,data)
            #if we get lucky and find the right node, return that node. 
            if currNode.data == data:
                return currNode
            else:
                currLevel = currLevel - 1
        
        currNode = self.findFirstNodeLessThanOrEqualTo(currNode, 0, data)
        if currNode == None or currNode.data != data:
            return None
        else:
            return currNode
        print("Error, should not have gotten here")
        return None

    #Removes a node with matching data from the skip list. Changes next/prev pointers at every layer of the skiplist if relevant. 
    def delete(self, data):
        node = self.findNode(data)
        if node == None:
            print("Error: cannot delete node that does not exist")
            return
        i = 0
        while i < self.levels:
            #if the node is not on this level, we're done.
            if node.nextPointers[i] == None and node.prevPointers[i] == None:
                break
            #if the node we're deleting is the head of this level, set the new head to be the next node.
            #Being the head is the same as not having a prev node. 
            if self.heads[i] == node:
                self.heads[i] = node.nextPointers[i]
                #the new head will have None as its prev pointer.
                self.heads[i].prevPointers[i] = None
                i = i+1
                continue
            #if there is a node before and after the current node
            if node.prevPointers[i] != None and node.nextPointers[i] != None:
                #set prev of the next node to the prev node
                node.nextPointers[i].prevPointers[i] = node.prevPointers[i]
                #set next of the prev node to the next node
                node.prevPointers[i].nextPointers[i] = node.nextPointers[i]
                i = i+1
                continue
            #if the node does not have a next node
            if node.nextPointers[i] == None:
                node.prevPointers[i].nextPointers[i] = None
                i = i+1
                continue
             
            
        
    #searches a 1d list, starting at the startNode, for a node with the given data.
    #Returns None if node is not found, otherwise returns the node.
    #Assumes the list is sorted in increasing order. 
    def findFirstNodeLessThanOrEqualTo(self, startNode,level,data):
        currNode = startNode
        if currNode == None:
            print("Error: null node used as starting node")
            return None
        if currNode.data > data:
            return None

        while currNode != None:
            #return the node if we find it.
            if currNode.data == data:
                return currNode
            #if the next node is bigger than the node we're looking for or None, return the current node.
            #the current node is the greatest node less than the node we're looking for.
            if currNode.nextPointers[level] == None:
                return currNode
            if currNode.nextPointers[level].data > data:
                return currNode
            #if the node we're looking for is greater than the current node, advance to the next node in the linked list.
            if currNode.data < data:
                currNode = currNode.nextPointers[level]


    #inserts a node at the linked list in the given level. 
    def insertIntoLevel(self, level, node):

        #if the current level is empty, make the node the new head.
        if self.heads[level] == None:
            node.nextPointers[level] = None
            node.prevPointers[level] = None
            self.heads[level] = node
            return

        #if the node is less than the head of the current level, make the node the new head.
        if node.data <= self.heads[level].data:
            #new node next is the old head. Prev is None.
            node.nextPointers[level] = self.heads[level]
            node.prevPointers[level] = None
            #old head prev is the new node
            self.heads[level].prevPointers[level] = node
            #new head of this level is the new node.
            self.heads[level] = node
            return
        
        currNode = self.heads[level]
        while currNode != None:
            #if currNode is the end of the list, put node after currNode. We already know node > currNode. 
            if currNode.nextPointers[level] == None:
                currNode.nextPointers[level] = node
                node.prevPointers[level] = currNode
                node.nextPointers[level] = None
                self.count = self.count + 1
                return
            if node.data <= currNode.nextPointers[level].data: #if the given node is less than the next node in the list
                node.nextPointers[level] = currNode.nextPointers[level] #set node next to be the next, bigger node.
                currNode.nextPointers[level].prevPointers[level] = node #set the next, bigger node's prev to be node.
                node.prevPointers[level] = currNode #set node prev to be the current (smaller) node. 
                currNode.nextPointers[level] = node #set the current node next to be the given node
                self.count = self.count + 1
                return #done, node inserted
            if node.data > currNode.data: #if the given node is bigger than currNode, advance currNode
                currNode = currNode.nextPointers[level]           
        return

    #prints the given level. 
    def printLevel(self, level):
        print("Printing level: ",level)
        currNode = self.heads[level]
        returnString = ""
        while currNode != None:
            returnString += str(currNode.data) +", "
            currNode = currNode.nextPointers[level]
        print(returnString)
            
    #prints the given level backwards 
    def printBackwards(self, level):
        print("Printing level: ",level, "backwards")
        currNode = self.heads[level]
        while currNode.nextPointers[level] != None:
            currNode = currNode.nextPointers[level]

        while currNode != None:
            print(currNode)
            currNode = currNode.prevPointers[level]

    #prints all levels. 
    def printAllLevels(self):
        i = 0
        while i < self.levels:
            self.printLevel(i)
            i = i + 1

def main():

    skiplist = SkipList(15)
    i = 0
    while i < 1000:
        skiplist.insert(i)
        i+=1
    
    skiplist.printAllLevels()




    
if __name__ == "__main__":
    main()
