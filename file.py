from page import Page

maxPages = 10

class PageMeta:
    def __init__(self, page: Page):
        self.table = page.tableName
        self.type = page.type
        self.len = page.length()
        try:
            page.availableId
            self.full = False
        except:
            self.Full = True
class File:
    def __init__(self, filename):
        fileExists = False
        self.fileName = filename
        self.pages = {} 
        self.pageIds = []
        try:
            f = open(self.fileName, "x")
        except:
            return
        
        self.loadFromFile()

    def loadFromFile():
        pass

    def availableId(self):
        if(len(self.pages.keys()) == maxPages ):
            raise Exception("File is full")
        
        for i in range(maxPages ):
            if( i not in self.pages.keys()):
                return i
    def getIds(self):
        ids = []
        for i in range(maxPages):
            if i in self.pages.keys(): 
                ids.append(i)
        
        return ids
    """
    creates header, stringifies pages and writes them down
    """
    def initializeFile(self):
        
        f = open(self.fileName, "w")

        pageStrings = {}
        for id in self.pages.keys():
            pageStrings[id] = self.pages[id].stringify()

        self.header = ""

        f.write(self.header)
        for pageId in self.pages.keys():
            f.write(pageStrings[pageId])

    def addPage(self, Page):
        self.pages[self.availableId()] = PageMeta(Page)
        self.updateHeader()

        f = open(self.fileName, "a")
        f.write(Page.stringify())
        f.close()


    def updateHeader (self):
        self.header = ""
        for pageId in range(len(self.pages.keys())):
            page = self.pages[pageId]
            self.header += page.table + "|"
            self.header += page.type + "|"
            self.header += str(page.len)
            isFull = page.full
            x = "0"
            if isFull:
                x = "1"
            self.header += "|" + x + "@"

        self.header = self.header[:-1]

        for i in range(1000 - len(self.header)):
            self.header += " "
        self.header += "\n"
        f = open(self.fileName, "r+")
        f.seek(0)
        f.write(self.header)
        f.close()
        
    def writePage(self):
        pass


f1 = File("halo.txt")
p = Page("table1", "record" , [int, int, str])
f1.addPage(p)
f1.addPage(p)
f1.addPage(p)
# f1.createPage("table2", "record" , [int, int, str, str])
# p = f1.getPage(0)
# p.insert([0,0,"halo"])
# p.insert([1,0,"halo"])
# p.delete(0)
# p.update(1, [1 , 1 , "updated"])
# p.insert([1,0,"halo"])
# f1.initializeFile()

print("lol")