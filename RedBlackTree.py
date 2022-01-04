class Node():
    def __init__(self, parent, left, right, color, data):
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color
        self.data = data

    def __str__(self):
        returnString = "Node with value: " + str(self.data)
        return returnString

    def setParent(self, parent):
        self.parent = parent

    def setLeft(self, leftChild):
        self.left = leftChild

    def setRight(self, rightChild):
        self.right = rightChild

    def setColor(self, color):
        self.color = color

    def isRightChildOf(self, node):
        if self.parent != node:
            return False
        if node.right == None:
            return False
        if node.right == self:
            return True
        return False

    def isLeftChildOf(self, node):
        if self.parent != node:
            return False
        if node.left == None:
            return False
        if node.left == self:
            return True
        return False

class BinarySearchTree():
    def __init__(self, root):
        self.root = root
        self.root.color = "black"
        self.size = 1

    def insert(self, data):
        node = Node(None,None,None,"red",data)
        self.size = self.size + 1
        currNode = self.root
        while currNode != None:
            if node.data <= currNode.data:
                if currNode.left != None:
                    currNode = currNode.left
                    continue
                else:
                    currNode.left = node
                    node.parent = currNode
                    return
            else:
                if currNode.right != None:
                    currNode = currNode.right
                    continue
                else:
                    currNode.right = node
                    node.parent = currNode
                    return

    def printTree(self, node):
        if node.left != None:
            self.printTree(node.left)
        returnString = "Node: " + str(node.data) + " Left Child: "
        if node.left != None:
            returnString = returnString + str(node.left.data) +" "+ node.left.color
        returnString = returnString + " Right Child: "
        if node.right != None:
            returnString = returnString + str(node.right.data) +" "+ node.right.color
        print(returnString)
        if node.right != None:
            self.printTree(node.right)

    def search(self, root, data):
        currNode = root
        while currNode != None:
            if data == currNode.data:
                return currNode
            if data < currNode.data and currNode.left != None:
                currNode = currNode.left
                continue
            if data > currNode.data and currNode.right != None:
                currNode = currNode.right
                continue
            return None

    def minimum(self, root):
        currNode = root
        while currNode.left != None:
            currNode = currNode.left
        return currNode

    def maximum(self, root):
        currNode = root
        while currNode.right != None:
            currNode = currNode.right
        return currNode

    def successor(self,data):
        currNode = self.search(self.root, data)
        if currNode == None:
            print("Error: Can't find successor of Node that does not exist")
            return
        if currNode.right != None:
            return self.minimum(currNode.right)
        if currNode.parent == None:
            return None
        while True:
            if currNode.parent == None:
                return None
            if currNode.isLeftChildOf(currNode.parent):
                return currNode.parent
            else:
                currNode=currNode.parent

    def predecessor(self, data):
        currNode = self.search(self.root,data)
        if currNode == None:
            print("Error: Can't find predecessor of Node that does not exist")
            return
        if currNode.left != None:
            return self.maximum(currNode.left)
        if currNode.parent == None:
            return None
        while True:
            if currNode.parent == None:
                return None
            if currNode.isRightChildOf(currNode.parent):
                return currNode.parent
            else:
                currNode=currNode.parent

    def leftRotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        elif x == x.parent.right:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        print("y.right = ", str(y.right))
        x.parent = y
        print("x.parent = ", str(x.parent))

    def rbInsert(self, z):
        z = Node(None,None,None,None,z)
        y = None
        x = self.root
        while x != None:
            y = x
            if z.data < x.data:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.data <= y.data:
            y.left = z
        else:
            y.right = z
        z.left = None
        z.right = None
        z.color = "red"
        self.rbFixup(z)

    def rbFixup(self, z):
        while z.parent != None and z.parent.color == "red":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if  y != None and y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                elif z == z.parent.right:
                    z = z.parent
                    self.leftRotate(z)
                if z.parent != None:
                    z.parent.color = "black"
                    if z.parent.parent != None:
                        z.parent.parent.color = "red"
                        self.rightRotate(z.parent.parent)
            elif z.parent == z.parent.parent.right:
                y = z.parent.parent.left
                if y!= None and y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    z.parent.parent.color = "red"
                    z = z.parent.parent
                elif z == z.parent.left:
                    z = z.parent
                    self.rightRotate(z)
                if z.parent != None:
                    z.parent.color = "black"
                    if z.parent.parent!= None:
                        z.parent.parent.color = "red"
                        self.leftRotate(z.parent.parent)
        self.root.color = "black"
                    

        
        

def main():
    root = Node(None, None, None, None, 26)
    BST = BinarySearchTree(root)
    BST.rbInsert(17)
    BST.rbInsert(14)
    BST.rbInsert(10)
    BST.rbInsert(7)
    BST.rbInsert(3)
    BST.rbInsert(12)
    BST.rbInsert(16)
    BST.rbInsert(15)
    BST.rbInsert(21)
    BST.rbInsert(19)
    BST.rbInsert(20)
    BST.rbInsert(23)
    BST.rbInsert(41)
    BST.rbInsert(47)
    BST.rbInsert(30)
    BST.rbInsert(28)
    BST.rbInsert(38)
    BST.rbInsert(35)
    BST.rbInsert(39)
    
    print(BST.maximum(BST.root))
    print(BST.minimum(BST.root))
    print(BST.search(BST.root, 12))
    print(BST.search(BST.root,13))
    print(BST.successor(16))
    print(BST.successor(BST.maximum(BST.root).data))
    print(BST.predecessor(3))
    print(BST.predecessor(7))
    

if __name__ == "__main__":
    main()

