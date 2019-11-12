var mosca = require('mosca');   // npm install mosca
var mongo = require('mongodb')  // npm i mongodb
var mongc = mongo.MongoClient
var url = 'mongodb://lintang:1234@localhost:27017/mqtt_lintang'

var server = new mosca.Server(settings);
var settings = {
    port:1883
}

server.on('published', function(packet, client) {
    // console.log('Published', packet.payload);
    console.log('Published:', packet.payload.toString());
    if(packet.payload.toString().slice(0,1) != '{' && packet.payload.toString().slice(0, 4) != 'mqtt'){
        mongc.connect(url, (error, client)=>{
            // console.log('Terhubung db!')
            var koleksi = client.db('mqtt_lintang').collection('mqtt')
            koleksi.insertOne({
                message: packet.payload.toString()
            }, () => {
                console.log('Data terkirim!')
                client.close()
            })
        })
    }
});

server.on('ready', function(){
    console.log("Broker is ready!");
});