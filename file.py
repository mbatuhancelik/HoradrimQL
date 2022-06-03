import os.path
import os
from page import Page

maxPages = 10
headerLen = 1000


class PageMeta:
    def __init__(self, table, type, len, full):
        self.table = table
        self.type = type
        self.len = len
        self.full = full


class File:
    def __init__(self, filename):
        self.fileName = filename

        self.exists = False
        self.pages = {}
        self.pageIds = []

        if os.path.exists(filename):
            self.exists = True
            self.loadFromFile()

    def loadFromFile(self):
        f = open(self.fileName, "r")
        header = f.readline()
        f.close()

        pages = header.split("@")
        for id in range(len(pages)):
            page = pages[id]
            metadata = page.split("|")
            id = int(metadata[0])
            self.pages[id] = PageMeta(
                metadata[1], metadata[2], int(metadata[3]), bool(int(metadata[4]))
            )
            self.pageIds.append(id)

    def availableId(self):
        if len(self.pages.keys()) == maxPages:
            raise Exception("File is full")

        max = len(self.pages)

        for i in self.pageIds:
            if i > max:
                max = i + 1

        return max

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
        self.exists = True
        f.close()

    def addPage(self, Page):
        if len(self.pages.keys()) >= maxPages:
            raise Exception(f"too many pages on file:{self.fileName}")
        id = self.availableId()
        str = Page.stringify()
        self.currentPage = Page
        self.pages[id] = PageMeta(Page.tableName, Page.type, len(str), Page.isFull())
        self.pageIds.append(id)

        self.updateHeader()

        f = open(self.fileName, "a")
        f.write(str)
        f.close()

        return id

    def updateHeader(self):

        self.header = ""
        for pageId in self.pageIds:
            page = self.pages[pageId]
            self.header += str(pageId) + "|"
            self.header += page.table + "|"
            self.header += page.type + "|"
            self.header += str(page.len)
            isFull = page.full
            x = "0"
            if isFull:
                x = "1"
            self.header += "|" + x + "@"

        self.header = self.header[:-1]

        for i in range(headerLen - len(self.header)):
            self.header += " "
        self.header += "\n"

        if not self.exists:
            self.initializeFile()
        f = open(self.fileName, "r+")
        f.seek(0)
        f.write(self.header)
        f.close()

    def updatePage(self, pageId, Page: Page):
        self.pages[pageId] = PageMeta(Page.tableName, Page.type,Page.length(), Page.isFull())
        self.updateHeader()
        f = open(self.fileName, "r+")
        chars = headerLen + 1
        ## this should take relative position of the page in the ids list
        for i in self.pageIds:
            if i == pageId:
                break
            chars += self.pages[i].len

        f.seek(chars)
        f.write(Page.stringify())
        f.close()
    
    def loadPageString(self, pageId):
        f = open(self.fileName, "r")
        chars = headerLen + 1
        ## this should take relative position of the page in the ids list
        for i in self.pageIds:
            if i == pageId:
                break
            chars += self.pages[i].len

        f.seek(chars)
        s = f.read(self.pages[pageId].len)
        f.close()
        return s
    def loadPage(self, pageId):
        
        s = self.loadPageString(pageId)
        p = Page("", "", "")
        p.loadFromString(s)

        return p
    def isFull(self):
        return len(self.pages.keys()) == maxPages
    def deletePage(self, pageId):
        ##TODO: keep the pages above the deleted page
        if pageId not in self.pageIds:
            raise Exception("Deleting nonexisting page")
        if len(self.pageIds) == 1:
            os.remove(self.fileName)
            return
        
        pageStrings = {}

        for i in self.pageIds:
            if not i == pageId:
                pageStrings[i] = self.loadPageString(i)
        
        self.initializeFile()
        self.pageIds.remove(pageId)
        del self.pages[pageId]
        self.updateHeader()

        f = open(self.fileName, "a")
        for i in self.pageIds:
            f.write(pageStrings[i])
        f.close()


# f1 = File("halo.txt")
# p = Page("table1", "record", [int, int, str, int, int, str])
# p.insert([0, 0, "halo",1, 0, "halo"])
# p.insert([1, 0, "halo",1, 0, "halo"])
# f1.addPage(p)
# p = Page("table2", "record", [int, int, str])
# p.insert([0, 0, "haloo"])
# p.insert([1, 0, "haloo"])
# f1.addPage(p)
# p = Page("table3", "record", [int, int, str])
# p.insert([0, 0, "halooo"])
# p.insert([1, 0, "halooo"])
# f1.addPage(p)
# # f1.addPage(p)
# f1.deletePage(1)
# # f1.createPage("table2", "record" , [int, int, str, str])
# # p = f1.getPage(0)
# # p.delete(0)
# # p.update(1, [1 , 1 , "updated"])
# # p.insert([1,0,"halo"])
# # f1.initializeFile()

# print("fml")
