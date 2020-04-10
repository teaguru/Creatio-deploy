import zipfile
import os.path
import os
import lxml.etree as ET
import pyodbc
import time
import psycopg2
import sys
# ARCHIVE UNPACKING MODULE


def inputpath():
    print('Enter path to the zip:')
    zippath = input()
    print(zippath)
    print(os.path.isfile(zippath))
    return(zippath)


def inputexportpath():
    print('Input export path')
    export_path = input()
    if os.path.exists(export_path):
        print(export_path)
        return(export_path)
    else:
        print('directory not exist, make it?(y/n)')
        answ = input()
        if (answ == 'y'):
            try:
                os.makedirs(export_path)
            except Exception as e:
                print('Got Exception', type(e), e.args, type(e.args))
                print("Создать директорию %s не удалось" % export_path)
            else:
                print("Успешно создана директория %s" % export_path)
                return(export_path)
        else:
            print('ERROR')
            sys.exit()


def export(zippath, exp_path):
    try:
        fantasy_zip = zipfile.ZipFile(zippath)
        fantasy_zip.extractall(exp_path)
        fantasy_zip.close()
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))
    else:
        print("sucessfull %s" % exp_path)



def read_connection(exp_path):
    string_path = exp_path + '\\' + 'ConnectionStrings.config'
    f = open(string_path, 'r+')
    for line in f:
        print(line)


def input_redis():
    print('input redis port between 0 and 85')
    flag = False
    while flag == False:
        port = input()
        if port.isdigit():
            port = int(port)
            if (port > 0 and port < 85):
                flag = True
                return port
            else:
                print("wrong port format, must be between 0 and 85")
        else:
            print("wrong format,not a number")


def input_subd():
    print('select database postgres[1] or mssql [2]')
    # here we make default names for database server, change it for your company
    defserv1 = "***"
    defserv2 = "***"
    defserv3 = "116.202.197.***"
    flag_subd = False
    while flag_subd == False:
        db_name = input()
        if int(db_name) == 1:
            print("Postgres")
            print("write postgres server adress, enter ip adress or server name. Also you can write 1 for the first default server{}".format(defserv3))
            servadr = input()
            if servadr == '1':
                servadr = defserv3
            print("Ok it will be", servadr)
            return("Postgres", servadr)
            flag_subd = True

        if int(db_name) == 2:
            print("write server adress, enter ip adress or server name. Also you can write 1 for the first default server{} or 2 for the second default server {}".format(defserv1, defserv2))
            servadr = input()
            if servadr == '1':
                servadr = defserv1
            if servadr == '2':
                servadr = defserv2
            print("Ok it will be", servadr)
            return("MSSQL", servadr)
            flag_subd = True
        else:
            print(" choose 1 or 2")


def input_db(bd):
    bd = bd
    print('write dbname')
    db_name = input()
    print("database is:", db_name)
    print(subd)
    if bd[0] == 'MSSQL':
        print('if you want to make Default connection for MSSQL database type "yes" or "y"')
        defcon = input()
        if (defcon == "yes") or (defcon == "y"):
            db = {'name': db_name, 'user': 'av*', 'password': '123654**'}
            return(db)
    print('input db user')
    db_user = input()
    print("user is:", db_user)
    print('input db password')
    db_psswd = input()
    print('******')
    db = {'name': db_name, 'user': db_user, 'password': db_psswd}
    return(db)


def read_connection(db, subd, redis_port, exp_path):
    string_path = exp_path + '\\' + 'ConnectionStrings.config'
    with open(string_path, encoding="utf-8") as f:
        tree = ET.parse(f)

        root = tree.getroot()

        for elem in root.getiterator():
            server = subd[1]
            if elem.attrib.get("name") == 'db':
                try:
                    if subd[0] == 'MSSQL':
                        sb_conn = "Data Source={}; Initial Catalog={}; Persist Security Info=True; MultipleActiveResultSets=True; user={}; password={}; Pooling = true; Max Pool Size = 100; Async = true; Connection Timeout=500".format(
                            server, db['name'], db['user'], db['password'])
                    else:
                        sb_conn = "Server={};Port=5432;Database={};User ID={};password={};Timeout=500; CommandTimeout=400;MaxPoolSize=1024;".format(
                            server, db['name'], db['user'], db['password'])

                    elem.attrib['connectionString'] = str(sb_conn)
                except Exception as e:
                    print('Got Exception', type(e), e.args, type(e.args))

            elif elem.attrib.get("name") == 'redis':
                try:
                    new_redis = "host=localhost;db={};port=6379;maxReadPoolSize=100;maxWritePoolSize=500".format(
                        redis_port)

                    elem.attrib['connectionString'] = new_redis

                except Exception as e:
                    print('Got Exception', type(e), e.args, type(e.args))
    try:
        tree.write(string_path, xml_declaration=True,
                   method='xml', encoding="utf-8")
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))


def dumpcheck(exp_path):
    try:
        pathdb = os.walk(exp_path + '\\db\\')
        for elem in pathdb:
            if len(elem[2]) == 1:
                pathdb = exp_path + '\\db\\' + str(elem[2][0])
                print(pathdb)
                return(True, pathdb)
            else:
                print('not one file in db directory')
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))


def open_dump(db, subd, pathdb):
    pathdb = pathdb[1]
    db = db
    subd = subd
    server = subd[1]
    database = db['name']
    username = 'avs'
    password = '12365***'
    try:
        cnxn = pyodbc.connect(('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                               server+';UID='+username+';PWD=' + password), autocommit=True)
        cursor = cnxn.cursor()
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))

    try:

        sql = "CREATE DATABASE {}".format(database)
        print(type(database))
        print('database {} will be created now'.format(database))
        cursor.execute(sql)
        print("created")
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))

    try:
        sql = "USE master; RESTORE DATABASE {} FROM DISK='{}' WITH RECOVERY, REPLACE ; ".format(
            database, pathdb)
        cursor.execute(sql)
        print(sql)
        time.sleep(5)

    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))
    cnxn.close()

# postgre database restoring module


def conndb():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="123654***",
        host="116.202.197.***",
        port="5432"
    )
    print(con)
    con.autocommit = True
    return(con.cursor())


def checkdb(con, testname):
    print("Database opened successfully")
    data = con.execute("select * from pg_database;")
    rows = con.fetchall()
    listx = list()
    for elem in rows:
        listx.append((elem[0]))
    print(listx)
    if testname in listx:
        print('Database name exist in the list,already')
        return(False)
    print('Name not in the list')
    return(True)


def createdb(exist, cur, testname):
    if exist == True:
        sql = "CREATE DATABASE {} WITH OWNER postgres  TEMPLATE template0;".format(
            testname)
        data = cur.execute(sql)
        if checkdb(cur, testname) == False:
            print("db $s created sucessfull".format(testname))
            return True
        else:
            print("db not created, check it mannualy")
            return False


def dumpcheck(exp_path):
    pathdb = os.walk(exp_path + '\\db\\')
    for elem in pathdb:
        if len(elem[2]) == 1:
            pathdb = exp_path + '\\db\\' + str(elem[2][0])
            print(pathdb)
            return(True, pathdb)
        else:
            print('not one file in db directory')


def dump_open(pathdb, cur, psql_path):
    if pathdb[0] == True:
        try:
            print("Database {} dump will be restoring into server, type password and wait".format(
                testname))
            os.system(
                psql_path + " -h 116.202.197.*** -p 5432  -U postgres -d  {}  {} ".format(testname, pathdb[1]))

        except Exception as e:
            print('Got Exception', type(e), e.args, type(e.args))
        finally:
            print('Success')


def db_create_postgre(exp_path, psql_path, testname):
    psql_path = psql_path
    exp_path = exp_path
    testname = testname
    con = conndb()
    # checking thant dbname is free
    exist = checkdb(con, testname)
    # creating new empty db
    createdb(exist, con, testname)
    # recieve path for db dump in creatio directory
    pathdb = dumpcheck(exp_path)
    dump_open(pathdb, con, psql_path)


if __name__ == '__main__':
    psql_path = "C:\\Progra~1\\PostgreSQL\\12\\bin\\pg_restore.exe"
    zippath = inputpath()
    exp_path = inputexportpath()
    export(zippath, exp_path)
    subd = input_subd()
    bd = input_db(subd)
    testname = bd['name']
    redis_port = input_redis()
    read_connection(bd, subd, redis_port, exp_path)
    print(subd[0])
    if subd[0] == 'Postgres':
        db_create_postgre(exp_path, psql_path, testname)
        print('oky')
    else:
        pathdb = dumpcheck(exp_path)
        open_dump(bd, subd, pathdb)
