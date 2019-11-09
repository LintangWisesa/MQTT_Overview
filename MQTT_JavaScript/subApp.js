var mqtt = require('mqtt')      // npm install mqtt
var client  = mqtt.connect('mqtt://localhost')

var topic = 'LINTANGtopic123'
client.on('connect', function () {
    client.subscribe(topic)
})

client.on('message', function (topic, message) {
    context = message.toString();
    console.log(context)
})