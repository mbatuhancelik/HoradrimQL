import sys
from table import Table
from logger import log
import os

args = sys.argv[1:]

inputFile = args[0]
outputFile = args[1]

inputFile =  inputFile
outputFile = outputFile

inputFile = open(inputFile, "r")
outputFile = open(outputFile, "w")

lines = [line for line in inputFile ]

os.chdir("2018400051_2018400252/src")
catalog = Table("_catalog", 1,["tableName"], [str])

def parseInput(line):
    command = line.split()
    if len(command) == 0: 
        return
    command_data = command[2:]
    if command[1] == "type":
        type_comm = command[0]
        if type_comm == "create":
            # Create a table
            type_name = command_data[0].strip()

            if catalog.tree.search(type_name):
                log(line, False)
                return
            num_fields = int(command_data[1].strip())
            primary_order = int(command_data[2].strip())

            command_data = command_data[3:]
            names = []
            types = []
            for i in range(0, len(command_data) -1, 2):
                names.append(command_data[i])
                type = int
                if "str" in command_data[i+1]:
                    type = str

                types.append(type) 
            Table(type_name, primary_order,names, types)
            catalog.insert([type_name])  
        if type_comm == "delete":

            type_name = command_data[0].strip()

            if not catalog.tree.search(type_name):
                log(line, False)
                return
            
            table = Table(type_name, None, None, None)
            table.deleteTable()

            catalog.delete(type_name)

        if type_comm == "list":
            res = catalog.list()

            if len(res) ==0:
                log(line, False)
                return

            for r in res:
                tempStr = ""
                for i in r:
                    tempStr += str(i) + " "
                tempStr += "\n"
                outputFile.write(tempStr)
    if command[1] == "record":
        record_comm = command[0]
        if record_comm == "create":
            type_name = command_data[0].strip()
            command_data = command_data[1:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)

            try:
                for i in range(len(table.fieldTypes)):
                    if table.fieldTypes[i] == int:
                        command_data[i] = int(command_data[i])
                
                table.insert(command_data)
            except:
                log(line, False)
                return
            

        if record_comm == "delete":
            # Delete the record in given table if exists
            type_name = command_data[0].strip()
            command_data = command_data[1:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)
            primaryValue = command_data[0]

            try:
                if table.primaryType == int:
                    primaryValue = int(primaryValue)
                table.delete(primaryValue)
            except:
                log(line, False)
                return
        if record_comm == "update":
            type_name = command_data[0].strip()
            command_data = command_data[2:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)

            try:
                for i in range(len(table.fieldTypes)):
                    if table.fieldTypes[i] == int:
                        command_data[i] = int(command_data[i])
                
                table.update(command_data)
            except:
                log(line, False)
                return
        if record_comm == "list":

            type_name = command_data[0].strip()
            command_data = command_data[1:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)
            try:
                result = table.list()

                if len(result) ==0:
                    raise Exception()

                for r in result:
                    tempStr = ""
                    for i in r:
                        tempStr += str(i) + " "
                    tempStr += "\n"
                    outputFile.write(tempStr) 
            except:
                log(line, False)
                return
        if record_comm == "search":
            type_name = command_data[0].strip()
            command_data = command_data[1:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)

            try:
                primaryValue = command_data[0]
                if table.primaryType == int:
                    primaryValue = int(primaryValue)
                r = table.search(primaryValue)
                if len(r) ==0:
                    raise Exception()
                tempStr = ""
                for i in r:
                    tempStr += str(i) + " "
                tempStr += "\n"
                outputFile.write(tempStr) 
            except:
                log(line, False)
                return
        if record_comm == "filter":
            # Filter record w.r.t the primary key
            type_name = command_data[0].strip()
            command_data = command_data[1:]
            if not catalog.tree.search(type_name):
                log(line, False)
                return

            table = Table(type_name, None, None, None)
            try:

                condition = command_data[0] 

                result = []
                if ">" in condition:
                    min = condition.split(">")[-1]

                    if table.primaryType == int:
                        min = int(min)
                    result = table.filter(min = min)
                if "<" in condition:
                    max = condition.split("<")[-1]

                    if table.primaryType == int:
                        max = int(max)
                    result = table.filter(max = max)
                if "=" in condition:
                    max = condition.split("=")[-1]

                    if table.primaryType == int:
                        max = int(max)
                    result = [table.search(max)]
                
                if len(result) ==0:
                    raise Exception()

                for r in result:
                    tempStr = ""
                    for i in r:
                        tempStr += str(i) + " "
                    tempStr += "\n"
                    outputFile.write(tempStr)
                
            except:
                log(line, False)
                return  
    log(line, True)  
    

for line in lines:
    parseInput(line.strip())

del catalog