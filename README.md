Связь с разработчиком teadev@yandex.ru

Supervisor.py - утилита для установки единого пароля на класете приложений CREATIO


Для изменения паролей на приложениях CREATIO с использованием PostgreSQL можно использовать скрипт на python:


Где "PASS" в функции conndb заменим на наш пароль на сервер СУБД


В переменную  host="000.000.000.000", подставим наш IP севревера


А supervisor_password  в функции main по аналогии на наш хэш пароля Supervisor ( чтоб его получить выполним sql запрос на приложении с нужным паролем):


SELECT "UserPassword" FROM "SysAdminUnit" WHERE  "Name" = 'Supervisor';



crinst.py - утилита для разворота приложений CREATIO из архива для MSSQL и POSTGRESQL. использовать на свой страх и риск;)
