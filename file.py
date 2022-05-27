from page import Page

maxPages = 10

class File:
    def __init__(self):
        self.pages = {} 

    def getPage(self, pageId):
        #TODO: load page from file
        return self.pages[pageId]

    def availableId(self):
        if(len(self.pages.keys()) == maxPages ):
            raise Exception("File is full")
        
        for i in range(maxPages ):
            if( i not in self.pages.keys()):
                return i

    def createPage(self, tableName, numFields, fieldTypes):
        self.pages[self.availableId()] = Page(tableName, numFields, fieldTypes)


f1 = File()
f1.createPage("table1", "record" , [int, int, str])
f1.createPage("table1", "record" , [int, int, str, str])
p = f1.getPage(0)
p.insert([0,0,"halo"])
p.insert([1,0,"halo"])
p.delete(0)
p.update(1, [1 , 1 , "updated"])

print("lol")