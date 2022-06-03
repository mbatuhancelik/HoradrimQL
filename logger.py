import time 

logFile = open("horadrim-Log.csv" , "a")

def log(operation, success: bool):
    status = "failure"
    if success:
        status = "success"
    logFile.write(  
        f"{int(time.time())},{operation},{status}"
    )