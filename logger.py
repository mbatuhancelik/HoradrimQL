import time 

logFile = open("horadrim-Log.csv" , "a")

def log(operation, success: bool):
    status = "failure"
    if success:
        status = "success"
    if operation[-1] =='\n':
        operation = operation[:-1]
    logFile.write(  
        f"{int(time.time())},{operation},{status} \n"
    )