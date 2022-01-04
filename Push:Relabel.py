#Graphs with adjacency matrix representation

class Vertex:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.height = 0
        self.excess = 0
        self.source = False
        self.sink = False

    def __str__(self):
        return "Vertex with key: " + str(self.key) + " Source: " + str(self.source) + " Sink: " + str(self.sink) + " Height: " + str(self.height) + " Excess: " + str(self.excess)
        

class Graph:
    def __init__(self, maxVertices):
        self.maxVertices = maxVertices
        self.numVertices = 0
        self.vertices = [None] * maxVertices

        #creates a VxV matrix to store edge weights.
        self.edges = []
        self.flows = []
        self.residualCap = []
        for i in range(maxVertices):
            col = []
            flowCol = []
            residCol = []
            for j in range(maxVertices):
                col.append(0)
                flowCol.append(0)
                residCol.append(0)
            self.edges.append(col)
            self.flows.append(flowCol)
            self.residualCap.append(residCol)

    #adds a new vertex to the graph. Vertices are just added consececutivley to the list
    #self.vertices, and have a key equal to their index in the list (0,1,2,...,self.maxVertices-1)
    def addVertex(self):
        if self.numVertices == self.maxVertices:
            print("Error: Can't add any more vertices to the graph")
            return
        self.vertices[self.numVertices] = Vertex(self.numVertices,self.numVertices)
        self.numVertices += 1

    def addEdge(self, u, v, weight):
        if self.vertices[u] == None or self.vertices[v] == None:
            print("Error: cannot add edge to vertex that does not exist")
            return
        self.edges[u][v] = weight

    def initializePreflow(self):
        #set the height and excess attribute of each vertex to be zero
        for vertex in self.vertices:
            vertex.height = 0
            vertex.excess = 0

        #for each edge, set the flow to be zero. If the edge does not exist, set the flow to be None.
        for i in range(self.maxVertices):
            for j in range(self.maxVertices):
                if self.edges[i][j] == 0:
                    self.flows[i][j] = None
                else:
                    self.flows[i][j] = 0
        
        #set the residual capacites to be equal to the edge matrix initially. I.e., if there is an edge from u to v and zero flow going down that edge,
        #the residual capacity of that edge is equal to the capacity of that edge. The residual capacity of that edge should decrease when flow is sent down that edge,
        #and the residual capacity of an imaginary edge going in the opposite direction should increase that same amount. 
        for i in range(self.maxVertices):
            for j in range(self.maxVertices):
                self.residualCap[i][j] = self.edges[i][j]
        
        #set vertex zero to be the source, and set its height to be the number of vertices
        self.vertices[0].source = True
        self.vertices[0].height = self.numVertices

        #set the final vertex to be the sink
        self.vertices[self.numVertices-1].sink = True

        for i in range(self.maxVertices):
            if self.edges[0][i] == 0: #if there is no edge from source to vertex i
                continue
            else: #if there is an edge from source to vertex i
                self.flows[0][i] = self.edges[0][i] #set the flow to be equal to the capacity of the edge
                self.residualCap[0][i] = 0 #if there is flow going from source to i equal to the weight of that edge, that edge is now saturated and should have a residual capacity of 0.
                self.residualCap[i][0] = self.flows[0][i] #if there is flow going from source to i, there is now an equal amount of residual capacity from i to source. 
                self.vertices[i].excess = self.flows[0][i] #set the excess of the vertex to be equal to the flow coming to it from the source.
                self.vertices[0].excess = self.vertices[0].excess - self.flows[0][i] #subtract the amount leaving from the source from the source's excess.
                #at the end of the algorithm, the absolute value of the source's excess will be the max flow.

    def push(self, u):
        vertex = self.vertices[u]
        if vertex.excess <= 0:
            print("No excess to push.")
            return
        if vertex.sink == True:
            print("Sink will never have excess, so it will never push")
            return


        #find the right vertex to push to
        v = None
        for i in range(self.numVertices):
            if self.vertices[i].height + 1 == self.vertices[u].height and self.residualCap[u][i] > 0:
                v = i
        if self.vertices[u].height != self.vertices[v].height +1:
            print("Height of u must equal height of v +1")
            return
        deltaF = min(self.residualCap[u][v], vertex.excess) #the amount of flow to move in this push is the minimum of the capacity left
        #in the edge from u to v, or however much excess is leftover.


        if self.edges[u][v] != 0:         #if there is a real edge from u to v
            self.flows[u][v] = self.flows[u][v] + deltaF #send flow down that edge equal to deltaF
            self.residualCap[u][v] = self.residualCap[u][v] - deltaF #when sending flow down an edge, reduce the residual capacity of that edge the same amount
            self.residualCap[v][u] = self.residualCap[v][u] + deltaF #when sending flow down an edge, increase the residual capacity of an edge in the opposite direction by that amount
        elif self.edges[v][u] != 0:
            #if there isn't an edge from u to v, but there is an edge from v to u, sending flow from u to v is the same as subtracting that same amount of flow
            #from v to u. 
            self.flows[v][u] = self.flows[v][u] - deltaF #reduce the amount of flow from v to u by deltaF
            self.residualCap[v][u] = self.residualCap[v][u] + deltaF #if reducing the amount of flow from v to u by delta F, increase the residual capacity by that amount
            self.residualCap[u][v] = self.residualCap[u][v] - deltaF #decrease the amount of residual capacity from u to v
        vertex.excess = vertex.excess - deltaF
        self.vertices[v].excess = self.vertices[v].excess + deltaF
        

    def relabel(self, u):
        vertex = self.vertices[u]
        if vertex.excess <= 0:
            print("No excess, so no relabel")
            return
        outNeighbors = []
        neighborHeights = []
        for i in range(self.numVertices):
            if self.residualCap[u][i] > 0:
                if vertex.height > self.vertices[i].height:
                    print("Error: There is capacity for flow from vertex ", u, " to vertex ", i)
                    return
                outNeighbors.append(self.vertices[i])
                neighborHeights.append(self.vertices[i].height)
        minHeight = min(neighborHeights)
        if vertex.height <= minHeight:
            vertex.height = minHeight +1
            return
        else:
            print("Error: vertex higher than all of its outneighbors")
            return

    def canPush(self, u):
        vertex = self.vertices[u]
        if vertex.excess <= 0:
            return False
        if vertex.sink == True:
            print("Sink will never push")
            return False
        for i in range(self.numVertices):
            if self.residualCap[u][i] > 0: #if there is capacity from vertex u to i
                if vertex.height == self.vertices[i].height+1: #if the height of the vertex is equal to an outneighbors height +1 
                    return True
        return False

    #you can relabel if there is excess, you can't push, and vertex u is a lower height than all of its neighbors that still have capacity.
    def canRelabel(self,u):
        vertex = self.vertices[u]
        heights = []
        if vertex.excess <= 0:
            return False

        if self.canPush(u):
            print("Can't relabel because can push")
            return False

        for i in range(self.numVertices):
            if self.residualCap[u][i] > 0: #if there is an edge from u to i with more capacity
                heights.append(self.vertices[i].height)
                if self.residualCap[u][i] > 0 and vertex.height > self.vertices[i].height: #this should have failed with the canPush check
                    print("There is capacity on the edge from (", str(u),",", str(i), ") and vertex ", str(u), " is higher than ", str(i))
                    return False
        maxHeight = max(heights)
        if vertex.height > maxHeight:
            print("vertex was higher than all of its neighbors already")
            return False

        return True


    def tryPushRelabel(self,u):
            if self.canPush(u):
                self.push(u)
                return True
            if self.canRelabel(u):
                self.relabel(u)
                return True
            return False
        
    #v1 is the lowest vertex that is not the source. vn is the highest vertex that is not the sink. 
    def pushRelabel(self, v1, vn):
        self.initializePreflow()

        i = v1
        streak = 0
        while True:
            if i == vn+1:
                i = v1
            if streak >= self.numVertices * 2:
                break
            if self.tryPushRelabel(i):
                i+=1
                streak = 0
                continue
            else:
                i+=1
                streak +=1
                continue

        print(self.vertices[0].excess)
            
            



def main():

    #make graph from page 726
    graph = Graph(6)
    #add 6 vertices labeled 0-5
    for i in range(6):
        graph.addVertex()
        
    #make vertex 0 the source and vertex 5 the sink. 
    graph.vertices[0].source = True
    graph.vertices[5].sink = True
    

    #add edges
    graph.addEdge(0,1,16)
    graph.addEdge(0,2,13)
    graph.addEdge(1,3,12)
    graph.addEdge(2,1,4)
    graph.addEdge(2,4,14)
    graph.addEdge(3,2,9)
    graph.addEdge(3,5,4)
    graph.addEdge(4,3,7)
    graph.addEdge(4,5,4)


    print("Edges:\n")
    print(graph.edges)
    print("Flows:\n")
    print(graph.flows)
    print("Residual Capacities:\n")
    print(graph.residualCap)
    for i in range(graph.maxVertices):
        print(graph.vertices[i])

    print("\n\n\n\n\n\n\n\n")


    graph.pushRelabel(1,4)


    print("Edges:\n")
    print(graph.edges)
    print("Flows:\n")
    print(graph.flows)
    print("Residual Capacities:\n")
    print(graph.residualCap)
    for i in range(graph.maxVertices):
        print(graph.vertices[i])
        

if __name__ == "__main__":
    main()
