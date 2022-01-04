class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None



class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def append(self, key, value):
        newNode = Node(key, value)
        if self.count==0:
            self.head = newNode
            self.tail = newNode
            self.count = self.count + 1
            return
        
        else: 
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
            self.count = self.count + 1
            return

    def popBack(self):
        if self.count == 0:
            raise RuntimeError("Can't pop an empty list")
        if self.count == 1:
            returnNode = self.tail
            self.head = None
            self.tail= None
            self.count = self.count - 1
            return returnNode
        else:
            returnNode = self.tail
            newTail = self.tail.prev
            newTail.next = None
            self.tail = newTail
            self.count = self.count - 1
            return returnNode

    def popFront(self):
        if self.count == 0:
            raise RuntimeError("Can't pop an empty list")
        if self.count == 1:
            returnNode = self.head
            self.head = None
            self.tail = None
            self.count = self.count - 1
            return returnNode
        else:
            returnNode = self.head
            newHead = self.head.next
            newHead.prev = None
            self.head = newHead
            self.count = self.count - 1
            return returnNode

    def printList(self):
        currNode = self.head
        while currNode != None:
            print("Key: ", currNode.key, " Value: ",currNode.value)
            currNode = currNode.next
            
    def printKeys(self):
        currNode = self.head
        while currNode != None:
            print(currNode.key)
            currNode = currNode.next

    def toString(self):
        currNode = self.head
        returnString = ""
        while currNode != None:
            returnString = returnString + str(currNode.key) + " " + str(currNode.value) + "\n"
            currNode = currNode.next
        return returnString

    def printReverse(self):
        currNode = self.tail
        while currNode !=None:
            print(currNode.value)
            currNode = currNode.prev
            
    def contains(self, key):
        if self.count == 0:
            return False
        currNode = self.head
        while currNode != None:
            if currNode.key==key:
                return True
            currNode = currNode.next
        return False

    def delete(self, key):
        if self.contains(key)==False:
            print("Error: Cannot delete because key not found")
            return
        if self.count == 0:
            print("Error: cannot delete because no keys in list")
            return
        if self.count==1:
            self.head = None
            self.tail = None
            self.count = 0
        currNode = self.head
        while currNode != None:
            if currNode.key==key:
                if currNode == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                    self.count = self.count -1
                    return
                if currNode == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None
                    self.count = self.count -1
                    return
                if currNode.prev != None and currNode.next != None:
                    currNode.prev.next = currNode.next
                    currNode.next.prev = currNode.prev
                    self.count = self.count - 1
                    return
                print("Should not ever see this")
        

    def get(self, key):
        if self.count == 0:
            print("Error: No keys in list")
        currNode = self.head
        while currNode != None:
            if currNode.key==key:
                return currNode
            currNode = currNode.next
        print("Error: key no found")

class HashTable:
    def __init__(self, hashSize):
        self.hashSize = hashSize
        self.keys = [None] * hashSize

#returns a large number based on the character passed in. 
    def charToInt(self, char):
        if char.lower() == 'a':
            return 1229 * 3*9
        if char.lower() == 'b':
            return 1381 * 3*11
        if char.lower() == 'c':
            return 1523 * 3 * 13
        if char.lower() == 'd':
            return 1663 * 3 * 15
        if char.lower() == 'e':
            return 1823 * 3 * 17
        if char.lower() == 'f':
            return 1993 * 3 * 19
        if char.lower() == 'g':
            return 2131 * 3 * 21
        if char.lower() == 'h':
            return 2131 * 3 * 23
        if char.lower() == 'i':
            return 2293 * 3 * 25
        if char.lower() == 'j':
            return 2437 * 3 * 27
        if char.lower() == 'k':
            return 2621 * 3 * 29
        if char.lower() == 'l':
            return 2749 * 3 * 31
        if char.lower() == 'm':
            return 2909 * 3 * 33
        if char.lower() == 'n':
            return 3083 * 3 * 35
        if char.lower() == 'o':
            return 3259 * 3 * 37
        if char.lower() == 'p':
            return 3433 * 3 * 39
        if char.lower() == 'q':
            return 3581 * 3 * 41
        if char.lower() == 'r':
            return 3733 * 3 * 43
        if char.lower() == 's':
            return 3911 * 3 * 45
        if char.lower() == 't':
            return 4073 * 3 * 47
        if char.lower() == 'u':
            return 4241 * 3 * 49
        if char.lower() == 'v':
            return 4421 * 3 * 51
        if char.lower() == 'w':
            return 4591 * 3 * 53
        if char.lower() == 'x':
            return 4759 * 3 * 55
        if char.lower() == 'y':
            return 5099 * 3 * 57
        if char.lower() == 'z':
            return 5281 * 3 * 59
        else:
            return 6143 * 3 * 61
        
#calculates a large number by adding up the charToInt values of all characters in
#the string. Then, mods that number by self.hashSize. 
    def wordToHashValue(self, word):
        wordValue = 0
        for element in range(0, len(word)):
            wordValue = wordValue + self.charToInt(word[element])
        return wordValue % self.hashSize

    def printHashTable(self):
        for i in range(0, self.hashSize):
                print("Index: ", i)
                if self.keys[i] != None:
                    self.keys[i].printList()

    def removePunctuation(self, string):
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        for ele in string:
            if ele in punc:
                string = string.replace(ele, "")
        return string.lower()

    def hashFile(self, filePath):
        position = 0
        with open(filePath, 'r') as file:
            for line in file:
                for word in line.split():
                    word = self.removePunctuation(word)
                    #check if word is already inserted. If so, increment count and continue
                    index = self.wordToHashValue(word)
                    if self.keys[index] != None and self.keys[index].contains(word):
                        self.increase(word)
                        continue
                    else:
                        self.insert(word, 1)

    def insert(self, key, value):
        index = self.wordToHashValue(key)
        if self.keys[index] == None:
            newList = LinkedList()
            newList.append(key,value)
            self.keys[index] = newList
            return
        if self.keys[index].contains(key) == False:
            self.keys[index].append(key, value)
            return
        if self.keys[index].contains(key) == True:
            self.keys[index].get(key).value = value
            return

    def delete(self, key):
        index = self.wordToHashValue(key)
        if self.keys[index] != None:
            self.keys[index].delete(key)

    def increase(self,key):
        index = self.wordToHashValue(key)
        if self.keys[index] != None:
            self.keys[index].get(key).value = self.keys[index].get(key).value + 1

    def listAllKeys(self):
        for i in range(0,self.hashSize):
            if self.keys[i] != None:
                self.keys[i].printKeys()
                
    def writeToFile(self, fileName):
        file = open(fileName, "w")
        for i in range(0, self.hashSize):
            if self.keys[i] != None:
                file.writelines(self.keys[i].toString())
        
    def find(self, key):
        index = self.wordToHashValue(key)
        if self.keys[index].contains(key) == True:
            return self.keys[index].get(key).value
        print("Key not found")
        return None
            

                    
                
        
