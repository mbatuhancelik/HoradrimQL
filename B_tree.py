


import json
from statistics import median_grouped

from numpy import isin


D = 4
leaves = []
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
                if not right:
                    right = self.data[i - 1]
                if not left:
                    left = self.data[i+1]
                self.data[i-1] = value
                self.data.insert(i-1, left)
                self.data.insert(i+1, right)
                return
        if not right:
            right = self.data[ -1]
        if not left:
            left = self.data[-3]
        self.data[-1] = left
        self.data.append(value)
        self.data.append(right)

    def toDict(self):
        d = {"isRoot": self.isRoot, "isLeaf": self.isLeaf, "rid" : self.rids}
        for i in range(len(self.data)):
            if isinstance(self.data[i], Node):
                d[i] = self.data[i].toDict()
            else:
                d[i] = self.data[i]
        return d

    def fromDict(self, d, keyType):
        self.isLeaf = d["isLeaf"]
        self.isRoot = d["isRoot"]
        self.rids = {}
        if keyType == int:
            for i in d['rid'].keys():
                self.rids[int(i)] = d['rid'][i]
        else:
            self.rids= d["rid"]

        del d["isLeaf"]
        del d["isRoot"]
        del d["rid"]
        ##TODO: sort keys
        for i in d.keys():
            if isinstance(d[i], dict):
                n = Node(False, False)
                n.fromDict(d[i], keyType)
                self.data.append(n)
            else:
                self.data.append(d[i])
        global leaves
        if self.isLeaf:
            leaves.append(self)

            
    def toJSON(self):
        return self.toDict()


class BTree:
    def __init__(self):
        self.root = Node(True, False)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
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
            right.leafInsert(node.data[2], node.rids[node.data[2]])
            right.leafInsert(node.data[3], node.rids[node.data[3]])
            right.leafInsert(node.data[4], node.rids[node.data[4]])
            left.next = right
            right.pre = left
            if(node.pre):
                node.pre.next = left
                left.pre = node.pre
            if node.next:
                node.next.pre = right
                right.next = node.next
            node.data.remove(toDivide)#_??
            del node.rids[toDivide]
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
                i = 0
                if node.isLeaf:
                    ended = True
                    break
                for i in range(1, len(node.data), 2):
                    if node.data[i] > value:
                        node = node.data[i -1]
                        self.stack.append(node)
                        break
                    elif  i + 2 >= len(node.data):
                        node  = node.data[i +1]
                        self.stack.append(node)
                        break
            

            
            self.stack.pop()
            self.__leafNodeInsert(node, value, rid)

    def __leafSearch(self,node, value):
        if value in node.data:
            return node.rids[value]
        else:
            return False
    def __indexSearch(self, node ,value):
        self.stack.append(node)
        if node.isLeaf:
            return self.__leafSearch(node,value)
        for i in range(1, len(node.data) -1, 2):
            if value < node.data[i]:
                return self.__indexSearch(node.data[i-1], value)

        return self.__indexSearch(node.data[len(node.data)-1],value)
    def search(self, value):
            if len(self.root.data) == 0:
                return False
            self.stack = []
            return self.__indexSearch(self.root, value)

    def __indexDelete(self, node):
        if node.isRoot:
            return
        if len(node.data)  < 3:
            raise Exception("Broken node while deleting ")
        if len(node.data) > 3:
            return
        
        parent = self.stack.pop()
        left = node.data[0]
        right = node.data[2]
        value = node.data[1]
        for i in range(1, len(parent.data), 2):
            if parent.data[i] > value:
                
                mergedNode = node.data + [parent.data[i]] + parent.data[i+1].data

                if len(mergedNode) == 2 * D + 1:
                    n = Node(False, False)
                    n.data = mergedNode
                    if parent.isRoot and len(parent.data) == 3:
                        n.isRoot = True
                        self.root = n
                    else:
                        parent.data.remove(parent.data[i-1])
                        parent.data.remove(parent.data[i-1])
                        parent.data[i-1] = n
                        self.__indexDelete(parent)
                else:
                    firstNode = mergedNode[:3*2 +1 + 1]
                    secondNode = mergedNode[3*2 +1 + 1:]
                    n1 = Node(False , False)
                    n1.data = firstNode
                    n2 = Node(False, False)
                    n2.data = secondNode

                    parent.data[i] = n2.data[1]
                    parent.data[i-1] = n1
                    parent.data[i+1] = n2
                return

        mergedNode =parent.data[-2].data +  [parent.data[-1]]+ node.data 
        if len(mergedNode) == 2 * D + 1:
            n = Node(False, False)
            n.data = mergedNode
            if parent.isRoot and len(parent.data) == 3:
                n.isRoot = True
                self.root = n
            else:
                parent.data.remove(parent.data[-1])
                parent.data.remove(parent.data[-1])
                parent.data[-1] = n
                self.__indexDelete(parent)
        else:
            firstNode = mergedNode[:3*2 +1 + 1]
            secondNode = mergedNode[3*2 +1 + 1:]
            n1 = Node(False , False)
            n1.data = firstNode
            n2 = Node(False, False)
            n2.data = secondNode

            parent.data[-2] = n2.data[1]
            parent.data[-3] = n1
            parent.data[-1] = n2


    def __leafDelete(self, node, value):
        if not node.isLeaf:
            raise Exception("Leaf deletion from non leaf node")
        node.data.remove(value)
        del node.rids[value]

        if len(node.data) == 1:
            parent = self.stack.pop()
            for i in range(1, len(parent.data) -1, 2):
                if value < parent.data[i]:
                    parent.data.remove(parent.data[i-1])
                    parent.data.remove(parent.data[i-1])
                    node.pre.next = node.next
                    node.next.pre = node.pre
                    self.stack.append(parent)
                    self.__leafNodeInsert(node.next, node.data[0], node.rids[node.data[0]])
                    if len(parent.data) == 3:
                        self.search(node.data[0])
                        self.stack.pop() #removing leaf node
                        self.stack.pop() #removing current node
                        self.__indexDelete(parent)
                    return
            i = len(parent.data)
            node.pre.next = node.next
            node.next.pre = node.pre
            self.stack.append(parent)
            parent.data.remove(parent.data[i-1])
            parent.data.remove(parent.data[i-2])
            self.__leafNodeInsert(node.pre, node.data[0], node.rids[node.data[0]])
            if len(parent.data) == 3:
                self.search(node.data[0])
                self.stack.pop() #removing leaf node
                self.stack.pop() #removing current node
                self.__indexDelete(parent)
            return

    def delete(self, value):
        self.stack = []
        rid = self.search(value)

        self.__leafDelete(self.stack.pop(), value)
    
    def loadFromDict(self, d, keyType):
        global leaves 
        leaves = []
        self.root.fromDict(d, keyType)
        for i in range(len(leaves) -1):
            leaves[i].next = leaves[i + 1]
            leaves[i + 1].pre = leaves[i]

        leaves[-1].pre = leaves[-2]
    def __listSubtree(self , node):
        max = node
        while not max.isLeaf:
            max = max.data[-1]

        min = node
        while not min.isLeaf:
            min = min.data[0]

        rids = {}
        node = min
        while node != max.next:
            for i in node.data:
                rids[i] = node.rids[i]
            node = node.next

    
        return rids
    def list(self):
        node = self.root
        while not node.isLeaf:
            node = node.data[0]

        rids = {}
        while isinstance(node, Node):
            for i in node.data:
                rids[i] = node.rids[i]
            node = node.next
    
        return rids

