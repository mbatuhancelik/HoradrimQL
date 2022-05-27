class Record: 
    def __init__(self, type, header, data  ):
        self.type = type
        self.header = header
        self.data = data 
    
    # def stringify (self):
    #     newStr = ""
    #     newStr += self.type
    #     newStr += "@"
    #     for h in self.header:
    #         newStr += self.header[h] + "|"
    #     newStr = newStr[:-1] + "@"
    #     for d in self.data:
    #         newStr += self.data[d] + "|"
    #     newStr = newStr[:-1]
    #     self.size  = len(newStr)
    #     return newStr