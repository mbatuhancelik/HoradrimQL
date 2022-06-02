import json
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
            self.tableName= d['tablename']
            types = d['fieldTypes']
            self.fieldTypes = []
            for t in types:
                if "int" in t:
                    self.fieldTypes.append(int)
                else:
                    self.fieldTypes.append(str)
            self.fileNames = d['fileNames'] 
            self.lastFile  = int(d['lastFile'])
            self.primaryOrder = int(d['primaryOrder'])
            self.primaryType = fieldTypes[primaryOrder]
            self.tree.loadFromDict(d['tree'], self.primaryType)
        self.fieldTypes = fieldTypes
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

        if self.tree.search(data[self.primaryOrder]):
            raise Exception("Key already exists")
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
            elif not file.isFull():
                p = Page(self.tableName, "record", self.fieldTypes)
                rid = p.insert(data)
                pageId = file.addPage(p)
                self.tree.insert(data[self.primaryOrder], (file.fileName, pageId, rid ))
                return
        self.lastFile += 1
        self.fileNames[self.lastFile] = (self.tableName + str(self.lastFile))
        file = File(self.fileNames[self.lastFile])
        p = Page(self.tableName, "record", self.fieldTypes)
        rid = p.insert(data)
        pageId = file.addPage(p)
        self.tree.insert(data[self.primaryOrder], (file.fileName, pageId, rid ))
    
    def update(self, data):
        key = data[self.primaryOrder]
        searchResult = self.tree.search(key)
        if searchResult:
            page = getPage(searchResult[0] , searchResult[1])
            page.update(searchResult[2], data)
            updatePage(page, searchResult[0], searchResult[1])
    
    def delete(self, key):
        searchResult = self.tree.search(key)
        if searchResult:
            page = getPage(searchResult[0] , searchResult[1])
            page.delete(searchResult[2])
            self.tree.delete(key)
            updatePage(page, searchResult[0], searchResult[1])
    def list(self):
        rids = self.tree.list()
        result = []
        for i in rids.keys():
            rid = rids[i] 
            p = getPage(rid[0], rid[1])
            result.append(p.records[rid[2]].data)
        return result
    def __del__(self):
        d = {'tree' : self.tree.root.toDict()}
        d['tablename'] = self.tableName
        types = []
        for t in self.fieldTypes:
            types.append(str(t))
        d['fieldTypes'] =types
        d['fileNames'] =self.fileNames 
        d['lastFile'] =self.lastFile 
        d['primaryOrder'] =self.primaryOrder
        filename = self.tableName + "_.json"
        outfile = open(filename,'w')
        json.dump(d, outfile, indent=4)
        outfile.close()


t = table("table1" , 1 , ["a" , "a" , "a"], [int, int, str])


for i in range(0, 300):
    if i == 24:
        print(i)
    t.insert([1,i,"0"])

for i in range(24, 48):
    if i == 26:
        print(i)
    t.delete(i)

del t
