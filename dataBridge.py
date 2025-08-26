import mysql.connector, csv, zipfile, os, datetime, decimal
from tabulate import tabulate

def writeLogMessage(message):
    with open('dataBridge.log','a') as logFile:
        logFile.write(f"[{str(datetime.datetime.now())[:19]}] {message}\n")

def writeLogError(error):
    with open('dataBridge.log','a') as logFile:
        logFile.write(f"[{str(datetime.datetime.now())[:19]}] ({str(type(error))[8:-2]}) -> ({error})\n")

mydb = mysql.connector.connect(user='root',passwd='ssaa',host='localhost')
mycursor = mydb.cursor()
def listDB():
    # Creating a List of Choosable Databases
    mycursor.execute('show databases')
    dbs = [i[0] for i in mycursor.fetchall() if i[0] not in ['information_schema','mysql','performance_schema','sys']]
    # Creating a Dictionary and mapping choices with DB names
    d_choice = dict([[i+1,v] for i,v in enumerate(dbs)])
    while True:
        print(tabulate(d_choice.items(),headers=['Choice','DB Name'],tablefmt='pretty'))
        choice = input("Enter your Choice or Press any Character to Exit: ")
        if choice.isdigit() and int(choice) in d_choice:
            return d_choice[int(choice)]
        elif not choice.isdigit():
            return 
        else:
            print("Invalid Choice ! Restarting... \n\n")

def listTable(database):
    mycursor.execute(f'use {database}')
    mycursor.execute('show tables')
    tables = [i[0] for i in mycursor.fetchall()]
    t_choice = dict([[i+1,v] for i,v in enumerate(tables)])
    while True:
        print(tabulate(t_choice.items(),headers=['Choice','Table Name'],tablefmt='pretty'))
        choice = input("Enter your Choice or Press any Character to Exit: ")
        if choice.isdigit() and int(choice) in t_choice:
            return t_choice[int(choice)]
        elif not choice.isdigit():
            return 
        else:
            print("Invalid Choice ! Restarting... \n\n")

def createZip():
    db = listDB()
    if db:
        path = input("Enter your Path or Press Enter to choose Current Diretory: ")
        newZip = zipfile.ZipFile(f'{path}\\{db}.zip','w') if path else zipfile.ZipFile(f'{db}.zip','w')
        mycursor.execute(f'use {db}')
        mycursor.execute('show tables')
        tables = [i[0] for i in mycursor.fetchall()]
        for table in tables:
            mycursor.execute(f'desc {table}')
            tableHeadings = [i[0] for i in mycursor.fetchall()]
            mycursor.execute(f'select * from {table}')
            tableRows = [i for i in mycursor.fetchall()]
            csvFile = open(f'{table}.csv','w',newline='')
            writer = csv.writer(csvFile)
            writer.writerow(tableHeadings)
            writer.writerows(tableRows)
            csvFile.close()
            newZip.write(f'{table}.csv')
            os.remove(f'{table}.csv')
        print("Zip File Created Successfully !!")
    else:
        print("Exiting")

def createTableCommand(heading,records,tableName):
    dataType = []
    if len(records) < 1 or heading == []:
        return
    for index,column in enumerate(records[0]):
        if column == '':
            try:
                i = 1
                while True:
                    column = records[i][index]
                    if column != '':
                        break
                    else:
                        i += 1
            except:
                column = ""
        if column.isdigit():
            if int(column) > 2147483647 or int(column) < -2147483648:
                dataType.append('bigint')
            else:
                dataType.append('int')
        else:
            try:
                temp = float(column)
                dataType.append('float')
            except:
                if len(column) == 10 and column[4] == '-' and column[7] == '-' and column[:4].isdigit() and column[5:7].isdigit() and column[8:].isdigit():
                    dataType.append('date')
                else:
                    dataType.append('varchar')
    if len(records[0]) == len(dataType):
        match_values = {}
        for i,v in enumerate(dataType):
            if v == 'varchar':
                match_values[i] = max([len(j[i]) for j in records]) + 20
        createTable = f'create table {tableName}('
        for i in range(len(heading)):
            if dataType[i] != 'varchar':
                createTable += f'{heading[i]}  {dataType[i]},'
            else:
                createTable += f'{heading[i]} {dataType[i]}({match_values[i]}),'
        createTable = createTable[:len(createTable)-1] + ')'
        return createTable
    else:
        return 
    
def insertIntoCommand(records,tableName):
    if records == []:
        return
    for r in range(len(records)):
        records[r] = [i if i != '' else None for i in records[r]]
    insertCommand = f"insert into {tableName} values"
    for i in records:
        if len(i) == 1:
            insertCommand += f"({i[0]}),"
        else:
            insertCommand += f"{tuple(i)},"
    insertCommand = insertCommand[:len(insertCommand)-1] 
    return insertCommand.replace('None','null')

def convertZip(createFile):
    zipPath = input("Enter the Absolute path with extension of the Zip File: ")
    try:
        zipFile = zipfile.ZipFile(zipPath,'r')
        csvFiles = [f for f in zipFile.namelist() if f.endswith('.csv')]
        print(f"\n\n{len(csvFiles)} CSV Files Found...")
        if len(csvFiles) > 0:
            dbName = zipFile.filename[:-4]
            if not createFile:
                while dbName:
                    try:
                        mycursor.execute(f'create database {dbName}')
                        mycursor.execute(f"use {dbName}")
                        break
                    except mysql.connector.errors.DatabaseError:
                        print("Database Already Exits...")
                        dbName = input("Give us a New Database Name or Press Enter to Exit: ")
                else:
                    print("Exiting...")
                    return
            else:
                destinationPath = input("Enter File Path or Press Enter for Current Directory: ")
                pythonFile = open(f"{destinationPath}\\{dbName}.py",'w') if destinationPath else open(f'{dbName}.py','w')
                pythonFile.write("import mysql.connector\n")
                host = input("Enter Host: ")
                user = input("Enter User: ")
                passwd = input("Enter Password: ")
                pythonFile.write(f"mydb = mysql.connector.connect(user='{user}',passwd='{passwd}',host='{host}',database='{dbName}')\n")
                pythonFile.write("mycursor = mydb.cursor()\n")
            leftTables = []
            for f in csvFiles:
                print(f"\nReading {f} File...")
                csvFile = zipFile.open(f)
                lines = (line.decode('utf-8') for line in csvFile)
                reader = csv.reader(lines)
                extraction = list(reader)
                heading = extraction[0]
                records = extraction[1:]
                createTable = createTableCommand(heading,records,csvFile.name[:-4])
                insertCommand = insertIntoCommand(records,csvFile.name[:-4])
                if createTable and insertCommand:
                    if not createFile:
                        mycursor.execute(createTable)
                        mycursor.execute(insertCommand)
                        mydb.commit()
                    else:
                        pythonFile.write(f'mycursor.execute("{createTable}")\n')
                        pythonFile.write(f'mycursor.execute("{insertCommand}")\n')
                elif heading != [] and not createFile:
                    while True:
                        print(f"\n\nThere is No Records in the {f} File !")
                        print("Thus We cannot Auto Detect the DataType of the Columns ...")
                        print("So, Do you want to Enter the DataType of Each Column including their Measures or We will just leave this file...")
                        option = input("Proceed Manual DataType Entering <y/n>: ")
                        if option.lower() == 'y':
                            dataType = []
                            for h in heading:
                                d = input(f"Enter Datatype of {h} Column: ")
                                dataType.append(d)
                            createTable = f"create table {csvFile.name[:-4]}("
                            for i in range(len(heading)):
                                createTable += f"{heading[i]} {dataType[i]},"
                            createTable = createTable[:len(createTable)-1] + ')'
                            try:
                                mycursor.execute(createTable)
                                mydb.commit()
                                break
                            except:
                                print("\nWrong DataType Entery Detected !!")
                                print(f"Reading {f} File Again...")
                                input("Press any Key to Continue..")
                        else:
                            print(f"{f} File Not Added to the Database !\n")
                            leftTables.append(f)
                            break
                else:
                    print(f"{f} File is Empty and Thus we cannot Create Table in the Database...")
                    print(f"{f} File Not Added to the Database !\n")
                    leftTables.append(f)
            if leftTables: print("\nThe Tables left without Adding into Database Are:")
            for t in leftTables:
                print(t)
            print("Thanks for using our Utility !")
            if createFile:
                pythonFile.write("mydb.commit()\n")
                pythonFile.write("mycursor.close()\n")
                pythonFile.write("mydb.close()")
                pythonFile.close()
                writeLogMessage(f"Created a Connectivity File: {dbName}.py")
            else:
                writeLogMessage(f"Created {dbName} Database")
        else:
            print("Exiting...")
    except Exception as e:
        writeLogError(e)
        print("Invalid Path / Invalid Extension ! \nPlease Check your Path...")
        print("Exiting...")

def csvToDB(createFile):
    while True:
        try:
            filePath = input("Enter Your File Name with Absolute Path with extension: ")
            f = open(filePath)
            while True:
                tableName = input("Enter Table Name: ")
                if tableName.isdigit():
                    print("\nTable Name Cannot be a Digit Alone !") 
                else:
                    break
            reader = csv.reader(f)
            extraction = list(reader)
            heading = extraction[0]
            records = extraction[1:]
            createTable = createTableCommand(heading,records,tableName)
            insertCommand = insertIntoCommand(records,tableName)
            if createTable and insertCommand:
                if createFile:
                    destinationPath = input("Enter File Path or Press Enter for Current Directory: ")
                    fileName = input("Enter File Name without Extention: ")
                    host = input("Enter Host: ")
                    user = input("Enter User: ")
                    passwd = input("Enter Password: ")
                    destinationDB = input("Enter the Database Name to Save: ")
                    newFile = open(f'{destinationPath}\\{fileName}.py','w') if destinationPath else open(f"{fileName}.py",'w')
                    newFile.write("import mysql.connector\n")
                    newFile.write(f"mydb = mysql.connector.connect(user='{user}',passwd='{passwd}',host='{host}',database='{destinationDB}')\n")
                    newFile.write("mycursor = mydb.cursor()\n")
                    newFile.write(f'mycursor.execute("{createTable}")\n')
                    newFile.write(f'mycursor.execute("{insertCommand}")\n')
                    newFile.write('mydb.commit()\n')
                    newFile.write("mycursor.close()\n")
                    newFile.write("mydb.close()\n")
                    newFile.close()
                    print(f"File Named {fileName}.py is Created Successfully !")
                    writeLogMessage(f"Created Connectivity File {fileName}.py")
                    print("Thanks for using our Utility !")
                    break
                else:
                    db = listDB()
                    if db:
                        mycursor.execute(f'use {db}')
                        mycursor.execute(createTable)
                        mycursor.execute(insertCommand)
                        mydb.commit()
                        writeLogMessage(f"Updated {db} Database")
                        print("Thanks for using our Utility !")
                        break
                    else:
                        print("Exiting...")
                        break
            else:
                print("There is No records in the Given File...")
                print("Table Cannot be Created into the MySQL Database !")
                print("Exiting...")
                break
        except Exception as e:
            writeLogError(e)
            print("Invalid Path / Invalid Extension ! \nPlease Check your Path...")
            print("Exiting...")
            break

def tableToCsv():
    dbName = listDB()
    if dbName:
        tableName = listTable(dbName)
        if tableName:
            try:
                destinationPath = input("Enter the Path to Save the File OR Press Enter to save it in Current Directory: ")
                csvFile = open(f"{destinationPath}\\{tableName}.csv",'w',newline='') if destinationPath else open(f"{tableName}.csv",'w',newline='')
            except Exception as e:
                writeLogError(e)
                print("Invalid Path / Invalid Extension ! \nPlease Check your Path...")
                print("Exiting...")
                return
            writer = csv.writer(csvFile)
            mycursor.execute(f"use {dbName}")
            mycursor.execute(f"desc {tableName}")
            writer.writerow([i[0] for i in mycursor.fetchall()])
            mycursor.execute(f"select * from {tableName}")
            writer.writerows(mycursor.fetchall())
            if not destinationPath: print(f"Your File {tableName}.csv Create Successfully on Current Directory !\n")
            else: print(f"Your File {tableName}.csv Create Successfully!\nIt is Complete Path is {destinationPath}\\{tableName}.csv\n")
            writeLogMessage(f"Created File {tableName}.csv")
            print("Thanks for using our Utility !")
            print("Exiting...")
    else:
        print("Exiting...")

def dbToFile():
    dbName = listDB()
    if dbName:
        mycursor.execute(f"use {dbName}")
        print(f"\nSelected Database: {dbName}")
        destinationPath = input("Enter the Path of the Python File to Create OR Press Enter to Save it in Current Directory: ")
        try:
            f = open(f"{destinationPath}\\{dbName}.py",'w') if destinationPath else open(f"{dbName}.py",'w')
        except Exception as e:
            writeLogError(e)
            print("Invalid Path Specified !")
            print("Exiting...")
            return
        f.write("import mysql.connector\n")
        print("\nNew DataBase Connection Initiation","----------------------------------",sep='\n')
        host = input("Enter Host: ")
        user = input("Enter User: ")
        passwd = input("Enter Password: ")
        print("----------------------------------\n")
        f.write(f"mydb = mysql.connector.connect(host='{host}',passwd='{passwd}',user='{user}')\n")
        f.write("mycursor = mydb.cursor()\n")
        f.write("#Creating the Database\n")
        f.write("mycursor.execute('create database {}')\n".format(dbName))
        f.write("#Using the Created Database\n")
        f.write("mycursor.execute('use {}')\n".format(dbName))
        mycursor.execute("show tables")
        tbls = [i[0] for i in mycursor]
        for tbl in tbls:
            f.write(f"#Creating {tbl} table and Inserting Records\n")
            mycursor.execute('show create table {}'.format(tbl))
            res = mycursor.fetchall()
            ctbl = ((res[0][1].replace('`','')).replace('\n',''))[:-64]
            f.write('mycursor.execute("{}")\n'.format(ctbl))
            mycursor.execute(f'select * from {tbl}')
            recs = mycursor.fetchall()
            new = []
            if recs != []:
                for rec in recs:
                    rec = list(rec)
                    for i in range(len(rec)):
                        if isinstance(rec[i],decimal.Decimal):
                            rec[i] = float(rec[i])
                        elif isinstance(rec[i],datetime.date):
                            rec[i] = str(rec[i])
                    rec = tuple(rec)
                    new.append(rec)
                stri = "insert into {} values".format(tbl)
                for rec in new:
                    stri += str(rec) + ','
                stri = stri[:-1] # Eliminating the last comma(,)
                f.write('mycursor.execute("{}")\n'.format(stri.replace('None','null')))
        f.write("mydb.commit()\n")
        f.write("mycursor.close()\n")
        f.write("mydb.close()\n")
        f.close()
        writeLogMessage(f"Created File {dbName}.py")
        print(f"The Database Coppied Successfully to the Destination Specified !")
        print("Thanks for using our Program !")
        print("Exiting...")
    else:
        print("Exiting...")

if __name__ == '__main__':
    print("\n\nWelcome to Data Bride - a MySQL and Python Utility")
    print('',"----------------------","Data Bridge Operations","----------------------",'',sep='\n')
    print("1. csv File to Python Connectivity File")
    print("2. Table to csv File")
    print("3. Add a Table to a Database using csv File")
    print("4. Create a Zip with all the Tables as csv Files")
    print("5. Integrate a Zip File with csv Files into the MySQL Local Server")
    print("6. Convert a Zip File with csv Files to Python Connectivity File")
    print("7. Convert a MySQL Database to a Python Connectivity File")
    print("8. Exit Program")
    choice = input("\nEnter your Choice: ")
    if not choice.isdigit():
        print("Invalid Input !")
        print("Exiting...")
    elif int(choice) == 1:
        csvToDB(True)
    elif int(choice) == 2:
        tableToCsv()
    elif int(choice) == 3:
        csvToDB(False)
    elif int(choice) == 4:
        createZip()
    elif int(choice) == 5:
        convertZip(False)
    elif int(choice) == 6:
        convertZip(True)
    elif int(choice) == 7:
        dbToFile()
    elif int(choice) == 8:
        print("Exiting...")
    else:
        print("Invalid Choice !")
        print("Exiting...")