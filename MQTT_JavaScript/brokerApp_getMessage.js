var mosca = require('mosca');   // npm install mosca
var settings = {
    port:1883
}

var server = new mosca.Server(settings);

server.on('published', function(packet, client) {
    // console.log('Published', packet.payload);
    console.log('Published:', packet.payload.toString());
});

server.on('ready', function(){
    console.log("Broker is ready!");
});