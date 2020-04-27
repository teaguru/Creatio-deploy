#Applicaton developed by Andrey Vsyakikh teadev@yandex.ru.
#Read guide in README

import psycopg2


def conndb(dbname):
    con = psycopg2.connect(
        database="{}".format(dbname),
        user="postgres2",
        password="PASS",
        host="000.000.000.000",
        port="5432"
    )
    print(con)
    con.autocommit = True
    return (con.cursor())


def changepass(cur, Supervisor_password):
    try:
        sql = ' UPDATE "SysAdminUnit" SET "UserPassword" = %(pass)s  WHERE "Name" = %(name)s;'
        data = cur.execute(sql, {'name': 'Supervisor', 'pass': Supervisor_password})
    except Exception as e:
        print('Got Exception', type(e), e.args, type(e.args))


def checkdb(con):
    print("Database opened successfully")
    con.execute("select datname from pg_database;")
    rows = con.fetchall()
    listx = list()
    for elem in rows:
       listx.append((elem[0]))

    print(listx)
    return (listx)


def cycledb(dblist, supervisor_password):
    for elem in dblist:
        if elem != 'postgres' and elem != 'template0' and elem != 'template1':
            con = conndb(elem)
            changepass(con, supervisor_password)


if __name__ == '__main__':
    supervisor_password = 'yKLOufQaK.f3Gwe5D9Fsdfgd3ZeXQOeE7xSXY2Z2ju2bzBIVd/1dHUznMq'
    dbname = 'postgres'
    con = conndb(dbname)
    dblist = checkdb(con)
    cycledb(dblist, supervisor_password)

