import logging
import asyncio
import os
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# pip install hbmqtt
from hbmqtt.broker import Broker   
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

logger = logging.getLogger(__name__)

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
        },
        'ws-mqtt': {
            'bind': '127.0.0.1:8080',
            'type': 'ws',
            'max_connections': 10,
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "passwd"),
        'plugins': [
            'auth_file', 'auth_anonymous'
        ]
    },
    'topic-check': {
        'enabled': False
    }
}

broker = Broker(config)

@asyncio.coroutine
def test_coro():
    yield from broker.start()
    #yield from asyncio.sleep(5)
    #yield from broker.shutdown()

@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://localhost/')
    # Subscribe to '$SYS/broker/uptime' with QOS=1
    yield from C.subscribe([
        ('LINTANGtopic/test', QOS_1),
        # ('$SYS/broker/load/#', QOS_2),
    ])
    logger.info("Subscribed")
    try:
        for i in range(1, 100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            # print("%d: %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
            # print(packet.payload.data)
            # print(str(packet.payload.data))
            print(packet.payload.data.decode("utf-8"))
            mydb = myclient["mqtt_lintang"]
            mycol = mydb["mqtt"]
            mydata = { "message": packet.payload.data.decode("utf-8") }
            x = mycol.insert_one(mydata)
            print('Data tersimpan!')
        # yield from C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
        # logger.info("UnSubscribed")
        # yield from C.disconnect()
    
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    #formatter = "%(asctime)s :: %(levelname)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(test_coro())
    asyncio.get_event_loop().run_until_complete(uptime_coro())
    asyncio.get_event_loop().run_forever()