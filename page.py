
from utils import padding
from record import Record

class Page:
    
    '''
    A page can store only one type of record!
    '''
    def __init__(self,tableName,type, fieldTypes):
        #TODO allocatte number of records in a page dynamically
        self.records = {int: Record}
        self.type = type
        self.tableName = tableName
        self.numFields = len(fieldTypes)
        self.fieldTypes = fieldTypes
        self.filled = [False] * 1024
        self.recordHeader = {"table": self.tableName}
    
    def availableId(self):
        if(len(self.records) == 1024):
            raise Exception("Page is full")
        
        for i in range(1024):
            if(not self.filled[i]):
                return i


    def validateData(self, data):
        if(len(data) != len(self.fieldTypes)):
            raise Exception(f"Field mismatch during page insert: Got {len(data)} while expecting {len(self.fieldTypes)}")
        for i in range(len(self.fieldTypes)):
            if not isinstance(data[i], self.fieldTypes[i]):
                raise Exception(f"Field mismatch during page insert: Got {type(data[i])} while expecting {self.fieldTypes[i]} at {i}")
    
    def insert(self, data):

        self.validateData(data)

        id = self.availableId()

        self.records[id] = Record(self.type ,self.recordHeader,data)

        self.filled[id] = True

    def update(self, id, data):
        self.validateData(data)

        self.records[id] = Record(self.type ,self.recordHeader,data)

    def delete(self, id):
        if id not in self.records.keys():
            raise Exception(f"Nonexisting record is deleted with id: {id}")

        del self.records[id]
        self.filled[id] = False 
    def length(self):
        return len(self.createHeader()) + (len(self.filled) * len(self.getIdString(0) + "#" + self.mockRecord() + "\n")) 
    def isFull(self):
        try:
            self.availableId()
            return False
        except:
            return True
    def getIdString(self, id):
        id = str(id)
        maxId = str(len(self.filled) -1)
        while not len(id) == len(maxId):
            id = "0" + id
        
        return id
    def mockRecord(self) :
        newStr = ""
        newStr += padding("")
        newStr += "@"
        for h in self.recordHeader:
            newStr += padding(h + "="+ "") + "|"
        newStr = newStr[:-1] + "@"
        for d in self.fieldTypes:
            newStr += padding("") + "|"
        newStr = newStr[:-1]
        return newStr
    def createHeader(self):
        newStr = ""
        
        newStr += self.type + "|"
        newStr += self.tableName + "|"
        newStr += str(self.numFields) + "|"
        for type in self.fieldTypes:
            newStr += str(type) + "#"

        newStr = newStr[:-1] + "|"
        x = None 
        for i in self.filled:
            if i:  
                x =  "1" 
            else: 
                x = "0"
            newStr += x 

        newStr += "^"
        self.header = newStr
        return newStr
    def stringify(self):
        newStr = self.createHeader()

        for i in range(len(self.filled)):
            if i in self.records.keys():
                newStr += self.getIdString(i) + "#" + self.records[i].stringify() + "-"
            else:
                newStr += self.getIdString(i) + "#" + self.mockRecord() + "-"
        
        return newStr

    def loadFromString(self, s):
        pass
