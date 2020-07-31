#!/bin/sh
PGHOST=localhost
PGPORT=5432
PGROLE=postgres
PGDATABASE=postgres

DATA=`date +"%Y-%m-%d_%H-%M"`
DATEFMT="%Y-%m-%d_%H-%M-%S"
GETDB="select datname from pg_database where datistemplate = 'f';"
SERVICELOG="/home/public/BACKUP/service.log"
BACKUPPATH="/home/public/BACKUP/files"
COUNT=0
TOTALCOUNT=0

echo "Start execution of backup databases script at ${DATA}" #>> ${SERVICELOG}

RESULT=$(/usr/bin/psql  -t -c "${GETDB}" 2>&1)
if [ $? -ne 0 ]; then
  echo "${RESULT}"
  exit
fi

for dbname in ${RESULT}; do
TOTALCOUNT=$((TOTALCOUNT + 1))
echo "`date +${DATEFMT}` Start backup ${dbname}" #>> ${SERVICELOG}
/usr/bin/pg_dump  ${dbname}| gzip > $BACKUPPATH/$DATA-${dbname}.sql.gz 2>&1
if [ $? -ne 0 ]; then
  echo "Failed to backup ${dbname}  \n" >> ${SERVICELOG}
  continue
else  
  echo "`date +${DATEFMT}` End backup ${dbname}  \n" >> ${SERVICELOG}
  COUNT=$((COUNT+1))
fi  
done    

/usr/bin/find $BACKUPPATH -type f -mtime +20 -exec echo "Removing outdated backup file: {}" \; -exec rm -f {} \;

echo "End execution of backup databases script at `date +${DATEFMT}`+ /\n" #>> ${SERVICELOG}
echo "${COUNT} of ${TOTALCOUNT} databases backed up  \n" #>> ${SERVICELOG}
echo "delete old backups at AWS"

aws --endpoint-url=https://storage.yandexcloud.net \
        s3 rm s3://postgre --recursive

echo "send new bacups to aws"

# send backuos to AWS yandex cloud, and notifications to slack
aws --endpoint-url=https://storage.yandexcloud.net \
    s3 cp --recursive /home/public/BACKUP/ s3://postgre > test.txt 2>&1
if grep "error" ./test.txt
then  /usr/bin/curl -vX POST --data-urlencode 'payload=  {"channel": "backups", "username":  "Admin", "text": "Будь осторожен!! Ошибки при заливки бэкапов в yandex cloud, проверь! :ultra_fast_parrot:"}' 'https://hooks.slack.com/services/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t'
fi;
if grep "upload:" ./test.txt
then  /usr/bin/curl -vX POST --data-urlencode 'payload=  {"channel": "backups", "username":  "Admin", "text": " :party-frog: Бэкапы залиты в облако успешно!"}' 'https://hooks.slack.com/services/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t'
fi
