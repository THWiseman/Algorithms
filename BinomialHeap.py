from LinkedList import Node
from LinkedList import LinkedList
import random

class BNode:
    def __init__(self, key, value):
        self.numChildren = 0
        self.key = key
        self.value = value
        self.parent = None
        self.children = []


    def addChild(self, childNode):
        childNode.parent = self
        self.children.append(childNode)
        self.numChildren = len(self.children)
        return

    def printFirstLayer(self):
        print("      Root: " + str(self.key))
        i = 0
        while i < self.numChildren:
            print("         Child order ", str(i) + ":")
            for j in self.children:
                if j.numChildren == i:
                    j.printTree()
            i+=1

    def printTree(self):
        print("                  " + str(self.key))
        for i in self.children:
            i.printTree()

    def printChildren(self,spacing):
        if self.children.count == 0:
            return
        returnString = ""
        for i in self.children:
            returnString += str(i.key) + " " * spacing
        print(returnString)
        for i in self.children:
            i.printChildren(spacing * 2)

    def minBFS(self, key):
        queue = []
        visited = []

        queue.append(self)
        visited.append(self)

        while queue:
            s = queue.pop(0)
            if key == s.key:
                return s
            for i in s.children:
                if i not in visited and i.key <= key:
                    queue.append(i)
                    visited.append(i)
        return None
        
    def __str__(self):
        return "BNode with key: " + str(self.key) + " Value: " + str(self.value) + " Num Children: " + str(self.numChildren)


class BinomialHeap:
    '''
    MaxOrder is the largest order tree possible for this Binomial heap. It should be suitably large and be about lg(n).
    Heads is a linked list of all of the roots of the binomial trees in the heap.
    Min is a pointer to the node with the lowest value seen so far.
    Each index in orders is a pointer to the tree of that order. e.g., self.orders[1] will have a binomial tree of size 2 there (if one exists)
    Size is the total number of nodes in the heap.
    '''
    def __init__(self, maxOrder):
        self.heads = []
        self.globalMin = None #Min is a pointers to the node with the smallest key
        self.maxOrder = maxOrder #how many orders this heap should contain. Should be bigger than lg(n). 
        self.orders = [None] * maxOrder #The heads of all the binomial trees. 

    '''   
    Add a new node to the heap. If self.orders[0] is empty, just put it there. If self.orders[0] is not empty but self.orders[1] is, combine them
    and put them there. Otherwise, recursively combine trees in order to fit this node.
    '''
    def push(self, key,value):
        newNode = BNode(key,value) #this is a tree of order 0 with the new node in it.
        
        if self.orders[0] == None: #If there is not yet an order 0 tree, just put the new tree at that spot. 
            self.orders[0] = newNode
            self.heads.append(newNode)
            if self.globalMin == None or newNode.key <= self.globalMin.key: #check to see if the new node is lower than the minimum.
                self.globalMin = newNode
            return

        #Since zero is not open, start by making a new tree that is a combination of the 0 tree and the newTree (which is another 0 tree).
        #Then, for each index, check if the next index is free. If it is, put that new combined tree there and delete entry of one of the trees that just got combined at the current index
        #(since it is now part of a bigger tree). If that next index is not free, combine the tempCombinedTree with the tree at that index, delete the tree at the current index, and repeat
        #with the index incremented by one. 
        else:
            i = 0
            tempCombinedTree = self.combineTrees(newNode, self.orders[0]) #the order 0 tree combined with the new node we just added (an order 1 tree)
            while i < self.maxOrder-1:
                if self.orders[i+1] == None:
                    self.orders[i+1] = tempCombinedTree
                    if self.globalMin == None or self.orders[i+1].key <= self.globalMin.key:
                        self.globalMin = self.orders[i+1]
                    return
                else:
                    tempCombinedTree = self.combineTrees(tempCombinedTree,self.orders[i+1])
                    i+=1
            print("Error adding value")

    '''
    self.globalMin should be updated by all the other operations that could change it. 
    '''
    def getMin(self):
        return self.globalMin
    
    '''
    For each head, if that head is less than the key we are looking for, BFS that head for the node we are looking for. Return it once found.
    This uses a special minBFS that will only look at items less than the head we are looking for. 
    '''
    def find(self, key):
        if key < self.globalMin.key:
            print("Error, key not found as it is less than the minimum")
            return
        for head in self.orders:
            if head == None:
                continue
            if head.key == key:
                return head
            if head.key > key:
                continue
            else:
                result = head.minBFS(key)
                if result != None:
                    return result
        print("Key not found in Heap")
        return None
            
    '''
    Saves the min, deletes the minimum from the heap, restores the Binomial heap property through a series of inserts, and then returns the min. Then, finds a new global min. 
    '''
    def extractMin(self):
        returnNode = self.globalMin
        tempList = []
        for child in self.globalMin.children:
            tempList.append(child)
        
        self.orders[self.globalMin.numChildren] = None
        self.heads.remove(self.globalMin)
        self.globalMin = None
        
        for child in tempList:
            self.insertTree(child, child.numChildren)
        
        for head in self.heads:
            if head != None:
                if self.globalMin == None or head.key < self.globalMin.key:
                    self.globalMin = head

        return returnNode

    '''
    Insert a tree of the specified order into the heap. If the index of that order is empty, just put that tree into that index and add the root to the list of heads.
    Otherwise, combine trees until the value is inserted. Basically the same as push, except it takes a node and its order (which should just be equal to its # of children) instead of a value. 
    '''
    def insertTree(self, root, order):
        if self.orders[order] == None:
            self.orders[order] = root
            self.heads.append(root)
            if self.globalMin == None or root.key < self.globalMin.key:
                self.globalMin = root
            return
        else:
            i = order
            tempCombinedTree = self.combineTrees(root, self.orders[i]) #This tree is a combination of the tree we're inserting and the tree of the same order already in the data structure.
            if self.orders[tempCombinedTree.numChildren] == None:
               self.orders[tempCombinedTree.numChildren] = tempCombinedTree
               return
            while i < self.maxOrder -1:
                if self.orders[i+1] == None:
                    self.orders[i+1] = tempCombinedTree
                    return
                else:
                    tempCombinedTree = self.combineTrees(tempCombinedTree, self.orders[i+1])
                    i+=1
        print("Error inserting tree")


    '''
    Locates a node with the matching key, and then changes that key to the newkey. If that newkey is less than the global min,
    updates the global min. Then, if the tree violates the minHeap property, it swaps up the new lower node until the property is no longer violated.
    If during the swapping the node gets swapped up to be the head of its order, updates the self.orders[] and self.heads[] to reflect that. 
    '''
    def decreaseKey(self, key, newKey):
        savedMin = self.globalMin
        if newKey >= key:
            print("Error, new key must be less than old key")
            return
        node = self.find(key)
        if node == None:
            print("Error, could not find node to decrease")
            return
        
        node.key = newKey


        while True:
            #if the node does not have a parent, we don't need to move it around at all since it's already the minimum. 
            if node.parent == None:
                if self.globalMin == None or node.key <= self.globalMin.key: #check to see if the new node is lower than the minimum.
                    self.globalMin = node
                    self.heads.append(node)
                    self.orders[node.numChildren] = node
                break
            #if the node's key is greater than its parents, we don't need to move it around at all.
            if node.key >= node.parent.key:
                break
            #if the nodes key is less than its parents, we need to swap it up a level. Also, if we replace the root of the tree, we need to update the orders and heads lists.
            if node.key < node.parent.key:
                if node.parent.parent == None: #We are about to swap the node to be the root of the tree.
                    childrenCopy = node.parent.children
                    self.heads.append(node)
                    self.heads.remove(node.parent)
                    node = self.swapNodeWithParent(node,node.parent)
                    self.orders[node.numChildren] = node
                    if self.globalMin == None or node.key <= self.globalMin.key:
                        self.globalMin = node
                        break
                else:
                    node = self.swapNodeWithParent(node,node.parent)
                    continue
    
                        

    
    def swapNodeWithParent(self, node, parent):
        if node == None or parent == None:
            print("Error: Node and parent must exist in order to swap")

        childrenCopy = node.children #copy all node data
        numChildrenCopy = node.numChildren
        parentCopy = node.parent
        if parentCopy != parent or node not in parent.children:
            print("Error: must swap node with its parent")
            return

        node.children = parent.children #replace all node data with that of its parent
        for child in node.children:
            child.parent = node
        node.children.remove(node) #remove the node from its own child list
        node.children.append(parent)
        node.numChildren = parent.numChildren
        
        node.parent = parent.parent #set the nodes new parent to its old grandparent.
        if node.parent != None:
            node.parent.children.remove(parent) #remove the nodes old parent from its old grandparent's list
            node.parent.children.append(node) #add the node to its old grandparents list

        parent.children = childrenCopy #update the parent to have all the data of the node.
        for child in parent.children:
            child.parent = parent
        parent.numChildren = numChildrenCopy
        parent.parent = node

        return node

    def delete(self, key):
        currentMin = self.globalMin
        node = self.find(key)
        if node == None:
            print("Error: could not find key to delete")
            return
        else:
            self.decreaseKey(key,-999)
            self.extractMin()
            self.globalMin = currentMin
            return
        

    #Compares two nodes and makes the smaller one the parent of the larger one. 
    def combineTrees(self, t1, t2):
        if t1.numChildren != t2.numChildren:
            print("Error: cannot combine trees with different orders")
            return
        if t1.key <= t2.key: #t1 will be the new root.
            self.orders[t1.numChildren] = None #since we're combining two trees of order x to an order x+1, we can delete the order x reference.
            t1.children.append(t2) #make t2 a child of t1
            t2.parent = t1
            t1.numChildren += 1
            if t2 in self.heads: #if t2 used to be a head, it just got sucked up so it wont be a head anymore. 
                self.heads.remove(t2)
            if t1 not in self.heads: #if t1 is not yet a head, it just became the root of a tree so add it to the list. 
                self.heads.append(t1)
            if self.globalMin == None or t1.key <= self.globalMin.key:
                self.globalMin = t1
            return t1
        else:
            self.orders[t2.numChildren] = None
            t2.children.append(t1)
            t1.parent = t2
            t2.numChildren +=1
            if t1 in self.heads:
                self.heads.remove(t1)
            if t2 not in self.heads:
                self.heads.append(t2)
            if self.globalMin == None or t2.key <= self.globalMin.key:
                self.globalMin = t2
            return t2

    def printHeap(self):
        i = 0
        while i < self.maxOrder:
            if self.orders[i] == None:
                print("Order " + str(i) + ": Empty\n")
                i+=1
                continue
            else:
                print("Order " + str(i) + ":")
                self.orders[i].printFirstLayer()
                print("\n")
                i+=1

    def printHeads(self):
        returnString = "Heads: "
        for i in self.heads:
            returnString += str(i.key) + " "
        print(returnString)

    def merge(self, other):
        for tree in other.heads: #for each tree on the other tree (the one we're trying to merge into this one)
            self.insertTree(tree,tree.numChildren)
                
        

def main():

    #Create a heap with orders 0 - 8
    heap = BinomialHeap(8)
    heap2 = BinomialHeap(8)

    inputList1 = []
    inputList2 = []
    i = 1
    while i < 50:
        inputList1.append(i)
        inputList2.append(i+50)
        i+=1

    #populate the heap
    for key in inputList1:
        heap.push(key,"hello")

    for key in inputList2:
        heap2.push(key*2,"hi")

    #display the heap
    print("Heap 1:")
    heap.printHeap()
    heap.printHeads()
    print("Heap 2:")
    heap2.printHeap()
    heap2.printHeads()

    #make nodes 10-20 negative (if present):
    
    i = 10
    while i <= 20:
        heap.decreaseKey(i,-i)
        i+=1
    

    #delete keys 20-30 (if present):
    i = 30
    while i <=30:
        heap.delete(i)
        i+=1
    
    #extract min a bunch of times  
    i = 0
    while i < 5 :
        print("Extract min: ", heap.extractMin().key)
        i+=1

    #combine heap1 and heap 2
    heap.merge(heap2)
    


    #display the heap
    print("Heap 1:")
    heap.printHeap()
    heap.printHeads()


if __name__ == "__main__":
        main()
            
            
        
