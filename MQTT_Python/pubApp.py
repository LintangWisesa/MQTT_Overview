import paho.mqtt.client as mqtt
# pip install paho-mqtt

client = mqtt.Client()
client.connect("localhost",1883,60)

while True:
    client.publish("LINTANGtopic/test", input('Message: '));
    # client.disconnect();
    # client.loop_forever()
