# pip install paho-mqtt
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("LINTANGtopic/test")

def on_message(client, userdata, msg):
    print(msg.payload.decode())

client = mqtt.Client()
client.connect("localhost",1883,60)

while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()