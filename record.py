from utils import padding
class Record: 
    def __init__(self, type, header: dict, data: list  ):

        self.type = type    # What are our record types 
        self.header = header
        self.data = data 
    
    
    def stringify (self):
        """Turn this record object to string."""
        newStr = ""
        newStr += padding(self.type)
        newStr += "@"
        for h in self.header:
            newStr += padding(h + "="+self.header[h]) + "|"
        newStr = newStr[:-1] + "@"
        for d in self.data:
            newStr += padding(str(d)) + "|"
        newStr = newStr[:-1]#??
        self.size  = len(newStr)# ??
        return newStr
    
    def loadFromString(self, s, types):
        """Fill a Record object with given string and types list(provides types of datas in record)"""

        data = s.split("@")
        self.type = data[0]

        #TODO: Decide on headers
        headers = data[1].split("|")
        for h in headers:
            header = h.split("=")
            self.header[header[0].strip()] = header[1].strip()

        data = data[2].split("|")
        if len(data) != len(types):
            raise Exception("Type number mismatch while loading records")
        for i in range(len(types)):
            data[i] = data[i].strip()
            if types[i] == int:
                data[i] = int(data[i])

        self.data = data
        