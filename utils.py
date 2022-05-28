fieldLength = 20

def padding(s: str):
        for i in range(fieldLength-len(s)):
            s = " " + s
        return s