from attr import validate
from record import Record

class Page:
    
    '''
    A page can store only one type of record!
    '''
    def __init__(self,tableName,type, fieldTypes):
        #TODO allocatte number of records in a page dynamically
        self.records = {}
        self.type = type
        self.tableName = tableName
        self.numFields = len(fieldTypes)
        self.fieldTypes = fieldTypes
        self.filled = [False] * 1024
    
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

        self.records[id] = Record(self.type ,{"table": self.tableName},data)

        self.filled[id] = True

    def update(self, id, data):
        self.validateData(data)

        self.records[id] = Record(self.type ,{"table": self.tableName},data)

    def delete(self, id):
        if id not in self.records.keys():
            raise Exception(f"Nonexisting record is deleted with id: {id}")

        del self.records[id]
        self.filled[id] = False
