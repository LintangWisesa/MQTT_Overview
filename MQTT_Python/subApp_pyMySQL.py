# pip install paho-mqtt
import paho.mqtt.client as mqtt
# pip install pymysql
import pymysql

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("LINTANGtopic/test")

def on_message(client, userdata, msg):
    print(msg.payload.decode())
    con = pymysql.connect(
        host='localhost',
        user='lintang',
        password='12345',
        db='mqtt_lintang',
        cursorclass=pymysql.cursors.DictCursor
    )
    kursor = con.cursor()
    sql = '''insert into mqtt (message) values (%s)'''
    val = str(msg.payload.decode())
    kursor.execute(sql, val)
    con.commit()
    print(kursor.rowcount, "Data tersimpan!")

client = mqtt.Client()
client.connect("localhost",1883,60)

while True:
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()