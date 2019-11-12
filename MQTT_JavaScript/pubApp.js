var mqtt = require('mqtt');     // npm install mqtt
var client  = mqtt.connect('mqtt://localhost');

var topic = 'LINTANGtopic123'
var message = 'Hello world!'

client.on('connect', function () {
    setInterval(function() {
        client.publish(topic, message);
        console.log('Message sent!', message);
    }, 5000);
});