fieldLength = 20

def padding(s: str):
    """
        Adds empty chars to the beginning of the string, in order to pad the string up until desired length.
    """
    for i in range(fieldLength-len(s)):
        s = " " + s
    return s