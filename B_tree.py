from calendar import isleap
from multiprocessing import parent_process


D = 4

class Node:
    def __init__(self, isRoot, isLeaf):
        self.data = []
        self.rids = {}
        self.isRoot = isRoot
        self.isLeaf = isLeaf  
        self.next = None
        self.pre = None

    def leafInsert(self, value, rid):
        if not self.isLeaf:
            raise Exception("you are inserting non pointer value to index node")
        self.rids[value] = rid
        self.data.append(value)
        self.data.sort()  
    def insert(self, value, right, left):
        if self.isLeaf:
            raise Exception("you are inserting pointer value to leaf node")
        if len(self.data) == 0:
            self.data = [left, value, right]
            return
        for i in range(1, len(self.data) , 2):
            if self.data[i] >  value:
                self.data[i-1] = value
                self.data.insert(i-1, left)
                self.data.insert(i, right)
                return
        
        self.data[-1] = left
        self.data.append(value)
        self.data.append(right)


class BTree:
    def __init__(self):
        self.root = Node(True, False)

    def __indexNodeInsert(self,node,value,right,left):
        # right left may be null
        node.insert(value,right, left)

        if len(node.data) > 2 * D + 1:
            toDivide = node.data[D + 1]
            left = Node(False, False)
            left.insert(node.data[1], left = node.data[0],right =  node.data[2])
            left.insert(node.data[3], left = node.data[2], right = node.data[4])
            right =Node(False, False)
            right.insert(node.data[7], left = node.data[6], right = node.data[8])
            right.insert(node.data[9], left = node.data[8], right = node.data[10])
            if len(self.stack) > 0:
                parent = self.stack.pop()
                self.__indexNodeInsert(parent, toDivide, right= right, left = left)
            else:
                root = Node(True, False)
                root.insert(toDivide, right=right, left=left)
                self.root.isRoot = False
                self.root = root

    def __leafNodeInsert(self,node,value, rid):
        
        node.leafInsert(value, rid)

        if len(node.data) > D:
            toDivide = node.data[int(D/2)]
            parent = self.stack.pop()

            left = Node(False, True)
            left.leafInsert(node.data[0], node.rids[node.data[0]])
            left.leafInsert(node.data[1], node.rids[node.data[1]])
            right =Node(False, True)
            left.leafInsert(node.data[2], node.rids[node.data[2]])
            left.leafInsert(node.data[3], node.rids[node.data[3]])
            left.leafInsert(node.data[4], node.rids[node.data[4]])
            left.next = right
            right.pre = left
            node.data.remove(toDivide)#_??
            self.__indexNodeInsert(parent,toDivide,right = right, left = left)


    def insert(self, value, rid):
        root = self.root

        self.stack = []
        self.stack.append(root)

        if len(root.data) == 0:
            left =  Node(False, True) 
            right = Node(False, True)
            right.pre = left
            left.next = right
            self.__indexNodeInsert(root, value,left = left, right = right)
            root.data[2].leafInsert(value, rid)
        else:
            node = root
            ended = False
            while not ended:
                for i in range(1, len(node.data), 2):
                    if node.data[i] > value:
                        node = node.data[i -1]
                        self.stack.append(node)
                        i = 1
                    if  i + 2 >= len(node.data):
                        node = node.data[i +1]
                        self.stack.append(node)
                        i = 1

                    if node.isLeaf:
                        ended = True
                        break
            
            self.stack.pop()
            self.__leafNodeInsert(node, value, rid)
            

t = BTree()
for i in range(6, 26):
    t.insert(i)

t.insert(27)


print("lol")