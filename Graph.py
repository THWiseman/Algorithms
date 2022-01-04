#Tree for BFS and DFS Code

class Clock:
    def __init__(self, startTime):
        self.time = startTime

    def tick(self):
        self.time+=1

    def time(self):
        return self.time
        

class GNode:

    def __init__(self, key, value): #
        self.inNeighbors = []
        self.outNeighbors = []
        self.inWeights = [] #need to figure out how to use a dictionary for this
        self.outWeights = []
        self.key = key
        self.value = value
        self.color = "white"
        self.predecessor = None #to be used in BFS and DFS
        self.distanceFromStart = 0 #to be used in BFS
        self.discoverTime = None # to be used in DFS
        self.finishTime = None# to be used in DFS

    def addDirectedEdge(self, other, weight): #adds directed edge from current node to another node
        self.outNeighbors.append(other)
        other.inNeighbors.append(self)
        #update the dictionary of edge weights to store the weight associated with this edge.

    def addUndirectedEdge(self, other,weight): #adds edges going to/from this node to/from other node.
        self.inNeighbors.append(other)
        self.outNeighbors.append(other)
        other.inNeighbors.append(self)
        other.outNeighbors.append(other)
        #update dictionaries of edge weights


    def __str__(self):
        return "Tree node with key: " + str(self.key) + " value: " + str(self.value)

class Graph:
    def __init__(self):
        self.nodes = []
        self.root = None #by default, the first node added will be the root.
        self.numNodes = 0

    def addNode(self, key,value):
        newNode = GNode(key,value)
        self.nodes.append(newNode)
        if self.root == None:
            self.root = newNode
        self.numNodes += 1

    def findNode(self,key): #returns the node with a key matching the provided key. 
        for node in self.nodes:
            if key == node.key:
                return node
        print("Error: Node with key: " + str(key) + " not found.")
        return None

    def addDirectedEdge(self, key1,key2,weight): #adds a directed edge from node1 to node2 with the specified weight. Make sure the nodes already exist in the graph!
        node1 = self.findNode(key1)
        node2 = self.findNode(key2)
        node1.addDirectedEdge(node2,weight)

    def addUndirectedEdge(self, key1,key2,weight): #add an undirected edge between node1 and node2 with the specified weight. Make sure the nodes already exist in the graph!
        node1 = self.findNode(key1)
        node2 = self.findNode(key2)
        node1.addUndirectedEdge(node2,weight)

    def printBFS(self,key): #prints out the path of a BFS starting at the node with the specified key. Will reset all nodes back to white once finished. 
        queue = []
        startNode = self.findNode(key)
        if startNode == None:
            print("Error, node not found. Aborting BFS")
            return
        startNode.distanceFromStart = 0
        startNode.color == "gray"
        queue.append(startNode)

        while queue:
            u = queue.pop(0)
            print(u)
            u.color = "gray"
            for node in u.outNeighbors:
                if node.color == "white":
                    node.color = "gray"
                    node.distanceFromStart = u.distanceFromStart + 1
                    node.predecessor = u
                    queue.append(node)
            u.color = "black"

        for node in self.nodes:
            node.color == "white"
            node.predecessor = None #might want to get rid of this later.

    def printDFS(self,key): #prints out the path of a DFS starting at the node with the specified key. Will reset all nodes back to white once finished. 
        startNode = self.findNode(key)
        if startNode == None:
            print("Error, node not found. Aborting DFS")
            return
        clock = Clock(0)
        print("Starting first DFS run")
        self.DFSVisit(startNode,clock) #most of the DFS should finish here

        '''
        numDFS = 2
        for node in self.nodes: #if any nodes weren't visited in the DFS, we will visit them here.
            print("Starting DFS run number: ", numDFS)
            if node.color == "white":
                self.DFSVisit(node,clock)
            numDFS +=1
        '''

    def DFSVisit(self,node, clock): #recursive helper function for DFS.
        clock.tick()
        node.discoverTime = clock.time
        print("Node: ", node.key, " discovered at ", node.discoverTime)
        node.color = "gray"
        for outNeighbor in node.outNeighbors:
            if outNeighbor.color == "white":
                outNeighbor.predecessor = node
                self.DFSVisit(outNeighbor, clock)
        node.color = "black"
        clock.tick()
        node.finishTime = clock.time
        #print("Node: ", node.key, " finished at ", node.finishTime)

    def DFSVisit(self,node, clock, helperList): #recursive helper function for topological sort.
        clock.tick()
        node.discoverTime = clock.time
        node.color = "gray"
        for outNeighbor in node.outNeighbors:
            if outNeighbor.color == "white":
                outNeighbor.predecessor = node
                self.DFSVisit(outNeighbor, clock)
        node.color = "black"
        clock.tick()
        node.finishTime = clock.time
        helperList.append(node.key)
        #print("Node: ", node.key, " finished at ", node.finishTime)

    def topologicalSort(self,key):
        startNode = self.findNode(key)
        if startNode == None:
            print("Error, node not found. Aborting DFS")
            return
        clock = Clock(0)

                
            

def main():
    
    #Create a graph
    graph = Graph()

    #add some nodes
    i = 0
    while i <= 9:
        graph.addNode(i, i)
        i+=1

    #add some edges
    graph.addDirectedEdge(1,2, 1)
    graph.addDirectedEdge(2,5, 1)
    graph.addDirectedEdge(1,4, 1)
    graph.addDirectedEdge(4,2, 1)
    graph.addDirectedEdge(3,5, 1)
    graph.addDirectedEdge(3,6, 1)
    graph.addDirectedEdge(6,6, 1)
    graph.addDirectedEdge(2,6, 1)

    #run a BFS
    graph.printDFS(1)

if __name__ == "__main__":
    main()
        
