from kafka import KafkaConsumer
import requests
import json
import getpass
# login_url for getting CRF CREATIO token
login_url = 'http://030130-studio.terrasoft.ru/ServiceModel/AuthService.svc/Login'
# service_url it`s our service address
service_url = 'http://030130-studio.terrasoft.ru/0/rest/UsrKafkaTestService/SetLookUp'
headers = {"Content-Type": "application/json"}
json_login = {"UserName": "Supervisor", "UserPassword": getpass.getpass()}
# kafka topic
topic = 'Testtopic'
# Recieve BPMCRF tocken here
resp = requests.post(login_url, headers=headers, json=json_login)
headers['BPMCSRF'] = resp.cookies.get_dict()['BPMCSRF']
consumer = KafkaConsumer('TestTopic',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])

# Starting Kafka listening
print('Server is listeng.......')

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    json = {"NameLookUp": "UsrKafkaLookUp", "ValueName": str(message.value.decode("utf-8"))}
    response = requests.post(service_url, headers=headers, cookies=resp.cookies, json=json)
    print(response.text)
# consume earliest available messages, don't commit offsets
KafkaConsumer(auto_offset_reset='earliest', enable_auto_commit=False)

# consume json messages
KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consume msgpack
KafkaConsumer(value_deserializer=msgpack.unpackb)

# StopIteration if no message after 1sec
KafkaConsumer(consumer_timeout_ms=1000)

# Subscribe to a regex topic pattern
consumer = KafkaConsumer()
consumer.subscribe(pattern='^awesome.*')

# Use multiple consumers in parallel w/ 0.9 kafka brokers
# typically you would run each on a different server / process / CPU
consumer1 = KafkaConsumer(topic,
                          group_id='my-group',
                          bootstrap_servers=['localhost:9092'])
