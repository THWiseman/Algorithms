import java.io.*;

//Created By Tom Wiseman 10/12/2021 for Algorithms Class

//Linked List Starter Code copied and modified from:
// https://www.geeksforgeeks.org/implementing-a-linked-list-in-java-using-class/

public class LinkedList {

    // Linked list Node.
    static class Node {
        int data;
        Node next;
        // Constructor
        Node(int d, Node next)
        {
            data = d;
            this.next = next;
        }

    }

    //Counts the number of nodes after and including the node provided.
    public static int size(Node node)
    {
        int count = 0;
        Node currNode = node;

        while(currNode!=null) {
            count = count+1;
            currNode = currNode.next;
        }

        return count;
    }

    // Method to print the LinkedList.
    public static void printList(Node node)
    {
        Node currNode = node;

        // Traverse through the LinkedList
        while (currNode != null) {
            // Print the data at current node
            System.out.print(currNode.data + " ");

            // Go to next node
            currNode = currNode.next;
        }
    }

    public static int findIntersection(Node headA, Node headB) {
        int diff = size(headA) - size(headB);
        if(diff>=0) {
            for(int i = 0; i<diff; i++) {
                headA = headA.next;
            }
        } else {
            for(int i = 0; i<-diff; i++) {
                headB = headB.next;
            }
        }
        while(headA != null) {
            if(headA==headB) {
                System.out.println(String.format("Intersection Node: %d", headA.data));
                return headA.data;
            }
            headA = headA.next;
            headB = headB.next;
        }
        return -1;
    }

    // Driver code
    public static void main(String[] args)
    {
        //List one goes Node 1,2,3,4,5,6,7,8,9,10
        Node node10 = new Node(10, null);
        Node node9 = new Node(9, node10);
        Node node8 = new Node(8, node9);
        Node node7 = new Node(7, node8);
        Node node6 = new Node(6, node7);
        Node node5 = new Node(5, node6);
        Node node4 = new Node(4,node5);
        Node node3 = new Node(3,node4);
        Node node2 = new Node(2, node3);
        Node node1 = new Node(1,node2);

        //List two goes Node 100,200,300,5,6,7,8,9,10
        Node node300 = new Node(300,node5);
        Node node200 = new Node(200, node300);
        Node node100 = new Node(100, node200);

        //print the lists to test
        System.out.println(String.format("List One:\n Size: %d",size(node1)));
        printList(node1);
        System.out.print("\n");
        System.out.println(String.format("List Two:\n Size: %d", size(node100)));
        printList(node100);
        System.out.print("\n");

        findIntersection(node100, node1);

    }
}