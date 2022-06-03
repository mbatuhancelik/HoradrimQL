
from utils import padding
from record import Record

class Page:
    
    '''
    A page can store only one type of record!
    '''
    def __init__(self,tableName,type, fieldTypes):
        #TODO allocatte number of records in a page dynamically
        self.records = {int: Record}    # <position in page, record>
        self.type = type
        self.tableName = tableName
        self.numFields = len(fieldTypes)
        self.fieldTypes = fieldTypes
        self.recordHeader = {"table": self.tableName}
        self.deleted = False
        self.size = int(2.5 * 1024 / len(self.mockRecord()))
        self.filled = [False] * self.size
    
    def availableId(self):
        if(len(self.records) == self.size):
            raise Exception("Page is full")
        
        for i in range(self.size):
            if(not self.filled[i]):
                return i


    def validateData(self, data):
        """Checking if given data's field length and types mathcing the expected."""

        if(len(data) != len(self.fieldTypes)):
            raise Exception(f"Field mismatch during page insert: Got {len(data)} while expecting {len(self.fieldTypes)}")
        for i in range(len(self.fieldTypes)):
            if not isinstance(data[i], self.fieldTypes[i]):
                raise Exception(f"Field mismatch during page insert: Got {type(data[i])} while expecting {self.fieldTypes[i]} at {i}")
    
    def insert(self, data):
        """ Insert the given record to page."""
        self.validateData(data)

        id = self.availableId()

        self.records[id] = Record(self.type ,self.recordHeader,data)

        self.filled[id] = True

        return id

    def update(self, id, data):
        """ Update existing record."""

        self.validateData(data)

        self.records[id] = Record(self.type ,self.recordHeader,data)

    def delete(self, id):
        """ Delete the record with given ID."""

        if id not in self.records.keys():
            raise Exception(f"Nonexisting record is deleted with id: {id}")

        del self.records[id]
        self.filled[id] = False
        self.deleted = True 
    def length(self):
        return len(self.createHeader()) + (len(self.filled) * len(self.getIdString(0) + "#" + self.mockRecord() + "\n")) 

    def isFull(self):
        """ Check if page has any available ID"""
        try:
            self.availableId()
            return False
        except:
            return True
    def getIdString(self, id):
        """ Padding given ID with 0's at the beginning, so that all ID's produce equal length strings"""

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
    def isEmpty(self):
        for b in self.filled:
            if b:
                return False
        return True
    def stringify(self):
        newStr = self.createHeader()

        for i in range(len(self.filled)):
            if i in self.records.keys():
                newStr += self.getIdString(i) + "#" + self.records[i].stringify() + "-"
            else:
                newStr += self.getIdString(i) + "#" + self.mockRecord() + "-"
        
        return newStr

    def loadFromString(self, s):
        s = s.split("^")
        if not len(s) == 2:
            raise Exception("Broken page while reading")
        
        header = s[0].split("|")
        data = s[1].split("-")

        self.tableName = header[1]
        self.recordHeader["table"] = self.tableName
        self.type = header[0]

        types = header[3].split("#")
        self.fieldTypes = []
        for i in range(int(header[2])):
            if "int" in types[i]:
                self.fieldTypes.append(int)
            else:
                self.fieldTypes.append(str)
        self.numFields = len(self.fieldTypes)
        self.size = len(header[4])
        self.filled = [False] * self.size

        for i in range(self.size):
            if header[4][i] == '1':
                record = data[i].split("#")
                self.records[int(record[0])] = Record("", {}, [])
                self.records[int(record[0])].loadFromString(record[1], self.fieldTypes)
                self.filled[i] = True
                
                

