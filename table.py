from cmath import inf
from fileinput import filename
import json
import pickle
from types import SimpleNamespace
from B_tree import BTree
from file import File
from page import Page
from buffermanager import getPage, updatePage
import os.path
class table:
    def __init__(self, tableName, primaryOrder, fieldNames,fieldTypes):
        

        self.tableName = tableName 
        filename = self.tableName + "_.json"
        self.tree = BTree()
        if os.path.exists(filename):
            infile = open(filename,'r')
            d = json.loads(infile.read())
            infile.close()
            self.tree.loadFromDict(d)
        self.fileNames = {}
        self.lastFile = 0
        self.fileNames[0] = (tableName + str(self.lastFile))
        self.primaryType = fieldTypes[primaryOrder]
        self.primaryOrder = primaryOrder
        if not os.path.exists(self.fileNames[0]):
            p = Page(tableName, "record", fieldTypes)
            f = File(self.fileNames[0])
            f.addPage(p)

    def insert(self,data):
        for i in self.fileNames.keys():
            file = File(self.fileNames[i])

            pageId = -1
            for p in file.pageIds:
                meta = file.pages[p]
                if not meta.full:
                    pageId = p
                    break
            
            if pageId > -1:
                page = getPage(file.fileName, pageId)
                rid = page.insert(data)
                self.tree.insert(data[self.primaryOrder], (file.fileName, pageId, rid ))
                updatePage(page, file.fileName, pageId)
                return
        self.lastFile += 1
        self.fileNames[self.lastFile] = (self.tableName + str(self.lastFile))
        f = File(self.fileNames[self.lastFile])
        p = Page(self.tableName, "record", self.fieldTypes)
        f.addPage(p)
        rid = page.insert(data, {"table":self.tableName})
        self.tree.insert(data[self.primaryOrder], (file.fileName, pageId, rid ))

    def __del__(self):
        print("kill me now")
        filename = self.tableName + "_.json"
        outfile = open(filename,'w')
        jsonStr = json.dump(self.tree.root.toDict(), outfile, indent=4)
        outfile.close()


t = table("table1" , 1 , ["a" , "a" , "a"], [int, int, str])
# t.insert([1,3,"0"])

t.insert([1,4,"0"])
t.insert([1,5,"0"])
t.insert([1,6,"0"])
t.insert([1,7,"0"])
print(t.tree.root.toDict())
print("lol")