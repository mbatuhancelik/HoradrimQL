import json
from B_tree import BTree
from file import File
from page import Page
from buffermanager import getPage, updatePage
import os.path
import os
class table:
    def __init__(self, tableName, primaryOrder, fieldNames,fieldTypes):
        
        self.deleted = False
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
            return
        self.fieldTypes = fieldTypes
        self.fileNames = {}
        self.lastFile = 0
        self.fileNames[0] = (tableName + "_"+ str(self.lastFile) )
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
        self.fileNames[self.lastFile] = (self.tableName + "_"+ str(self.lastFile) )
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
        keys = list(rids.keys())
        keys.sort()
        for i in keys:
            rid = rids[i] 
            p = getPage(rid[0], rid[1])
            result.append(p.records[rid[2]].data)
        return result
    def filter(self,min = None, max = None):
        if min and max : 
            raise Exception("Make your mind about filter")
        rids = self.tree.filter(min= min, max = max)
        result = []
        keys = list(rids.keys())
        keys.sort()
        for i in keys:
            result.append(getPage(rids[i][0],rids[i][1]).records[rids[i][2]])


        return result
    def deleteTable(self):
        for i in self.fileNames:
            os.remove(self.fileNames[i])
        filename = self.tableName + "_.json"
        if os.path.exists(filename):
            os.remove(self.tableName + "_.json")
        ##TODO: Remove yoursef from system catalog
        self.deleted = True
    def __del__(self):
        if self.deleted:
            return
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


t = table("table2" , 1 , ["asfasdsa"] * 12, [int] * 12)
t.deleteTable()


del t
