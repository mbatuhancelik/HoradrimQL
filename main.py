


from ast import Num


def parseInput(line):
    command = line.split()
    command_data = command[2:]
    if command[1] == "type":
        type_comm = command[0]
        if type_comm == "create":
            # Create a table
            type_name = command_data[0].strip()
            num_fields = command_data[1].strip()
            primary_order = command_data[2].strip()
            print(num_fields)
            for i in range(int(num_fields)):
                print(command_data[i+2])
            pass
        if type_comm == "delete":
            # Delete the table if exists
            pass
        if type_comm == "list":
            # List all tables
            pass
    if command[1] == "record":
        record_comm = command[0]
        if record_comm == "create":
            # Create record in given table
            pass
        if record_comm == "delete":
            # Delete the record in given table if exists
            pass
        if record_comm == "list":
            # List all record in given table with all fields
            pass
        if record_comm == "update":
            # Find and Update the given record in given table
            # first given value is primary key
            pass
        if record_comm == "search":
            # Find the given record in given table
            pass
        if record_comm == "filter":
            # Filter record w.r.t the primary key
            pass    
    




f = open("input.txt", "r")
lines = [line for line in f ]

parseInput(lines[0])