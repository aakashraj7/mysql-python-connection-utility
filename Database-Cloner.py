import mysql.connector
import decimal
import datetime
mydb = mysql.connector.connect(host='localhost',passwd='ssaa',user='root')
if mydb.is_connected():
    while True:
        print("+--------------------------------------------------------------------------------+")
        print("|                                DATABASE CLONER                                 |")
        print("+--------------------------------------------------------------------------------+")
        mycursor = mydb.cursor()
        mycursor.execute('show databases')
        dbs = [i[0] for i in mycursor]
        db = input("| Enter the Database Name to Copy: ")
        if db.lower() in dbs:
            mycursor.execute(f"use {db}")
            fname = input("| Enter your File Name: ")
            print("|","| Path Specification","| ------------------","|",sep='\n')
            print("| 1. Save in the same Direcotry")
            print("| 2. Specify Complete Path")
            try:
                choice = int(input("| Enter your Choice <1/2>: "))
                if choice  == 1:
                    f = open(f'{fname}.py','w')
                elif choice == 2:
                    path = input("| Enter the Path to Save: ")
                    f = open(r'{}\{}.py'.format(path,fname),'w')
                else:
                    print('| Invalid Choice !')
                    print('| Restrating Program...')
                    continue
            except:
                print('| Invalid Choice !')
                print('| Restrating Program...')
                continue
            f.write("import mysql.connector\n")
            print("|","| New DataBase Connection Initiation","| ------------------","|",sep='\n')
            host = input("| Enter Host: ")
            user = input("| Enter User: ")
            passwd = input("| Enter Password: ")
            f.write(f"mydb = mysql.connector.connect(host='{host}',passwd='{passwd}',user='{user}')\n")
            f.write("mycursor = mydb.cursor()\n")
            f.write("#Creating the Database\n")
            f.write("mycursor.execute('create database {}')\n".format(db))
            f.write("#Using the Created Database\n")
            f.write("mycursor.execute('use {}')\n".format(db))
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
                    f.write('mycursor.execute("{}")\n'.format(stri))
            f.write("mydb.commit()\n")
            f.write("mycursor.close()\n")
            f.write("mydb.close()\n")
            f.close()
            print(f"| The Database Coppied Successfully to the Destination Specified !")
            print("| Thanks for using our Program !")
            print("| Exiting...")
            break
        else:
            print("| The datbase {} doesn't exist !!".format(db))
            if input("| Do you want to Retry <y/n>: ").lower() != 'y':
                print("| Thanks for using our Program !")
                print("| Exiting...")
                break
            print("| Restarting Program...")
    print("+--------------------------------------------------------------------------------+")

