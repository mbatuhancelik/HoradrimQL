from utils import padding
class Record: 
    def __init__(self, type, header: dict, data: list  ):
        self.type = type
        self.header = header
        self.data = data 
    
    def stringify (self):
        newStr = ""
        newStr += padding(self.type)
        newStr += "@"
        for h in self.header:
            newStr += padding(h + "="+self.header[h]) + "|"
        newStr = newStr[:-1] + "@"
        for d in self.data:
            newStr += padding(str(d)) + "|"
        newStr = newStr[:-1]
        self.size  = len(newStr)
        return newStr