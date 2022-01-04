# Algorithms

All code written by me in Spring and Summer 2021 for CS5800 Graduate Algorithms or CS5004 Data Structures/Algorithms at Northeastern University. Each file can be run or compiled independently from the rest. The main() functions of the code demonstrates the algorithm is working through various examples and print statements.

# Files

- BinomialHeap.py: Very efficient implementation of a priority queue. Most operations are O(1) or O(lgn) time. 

- Graph.py: Simple way to represent relationships between nodes of data existing at different places in memory. Depth fist search and Breadth first search implemented. 

- HashTable.py: Stores data as key/value pair, where the key can be used to gain near O(1) access to its value, assuming a good hash function and minimal collisions. This program hashes AliceInWonderland.txt to count the number of times each word appears. 

- IntersectionOfLinkedLists.java: Finds the node at which two linked lists merge. Uses the fact that the common node will not be found in the longer list before a number of nodes equal to the difference in length of the two lists is skipped in that longer list. 

- LinkedList.py: Simple way to store data in non-continguous memory. This list is doubly linked and most operations take O(n) time. 

- Push:Relabel.py: Algorithm for finding the maximum flow in a flow network. Runs on O(V^2E) time complexity. Assume we are pushing flow from a source to a sink node, initialize the source node to a height equal to the number of vertices in the graph, and initialize all other heights to zero. Perform push() operations while you can, which pushes flow from nodes with excess to nodes with a smaller height. Relabel if pushing is not possible. 

-RedBlackTree.py: Essentially a Binary Search Tree that ensures that the tree will remain balanced, even when given adversarial data. All operations guarenteed to have upper bound of O(logn) time, while binary trees, in an adversarial case, can have operations that take O(n) time. 

-SkipList.py: Clever implementation of a sorted linked list that enables skipping of many nodes when performing operations that would take O(n) time in a normal linked list. With some duplication of data, we can create "express lanes" to traverse chunks of the linked list, skipping the need to visit every node. 

-sort.c: Basic implementation of insertion sort in C. 


