import psycopg2

def conndb(dbname):
    con = psycopg2.connect(
        database="{}".format(dbname),
        user="postgres2",
        password="12365000",
        host="116.202.197.000",
        port="5432"
    )
    print(con)
    con.autocommit = True
    return (con.cursor())


def changepass(cur, dbname, Supervisor_password):
    try:
        sql = ' UPDATE "SysAdminUnit" SET "UserPassword" = %(pass)s  WHERE "Name" = %(name)s;'
        data = cur.execute(sql, {'name': 'Supervisor', 'pass': Supervisor_password})
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))

def checkdb(con):
    print("Database opened successfully")
    data = con.execute("select datname from pg_database;")
    rows = con.fetchall()
    listx = list()
    for elem in rows:
        dbname = elem[0]
        listx.append((elem[0]))

    print(listx)
    return (listx)

def cycledb(dblist, Supervisor_password):
    for elem in dblist:
        if elem != 'postgres' and elem != 'template0' and elem != 'template1':
            print(elem)
            con = conndb(elem)
            changepass(con, elem, Supervisor_password)


if __name__ == '__main__':
    Supervisor_password = 'yKLOufQaK.f3Gwe5D9Fsdfgd3ZeXQOeE7xSXY2Z2ju2bzBIVd/1dHUznMq'
    dbname = 'postgres'
    con = conndb(dbname)
    dblist = checkdb(con)
    cycledb(dblist, Supervisor_password)


