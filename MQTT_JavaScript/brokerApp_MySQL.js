var mosca = require('mosca');   // npm install mosca
var mysql = require('mysql')    // npm i mysql
var settings = {
    port:1883
}

var server = new mosca.Server(settings);
var db = mysql.createConnection({
    host: 'localhost',
    user: 'lintang',
    password: '12345',
    database: 'mqtt_lintang'
})
db.connect(()=>{
    console.log('Database terhubung!')
})

server.on('published', function(packet, client) {
    // console.log('Published', packet.payload);
    console.log('Published:', packet.payload.toString());
    if(packet.payload.toString().slice(0,1) != '{' && packet.payload.toString().slice(0, 4) != 'mqtt'){
        var dbStat = 'insert into mqtt set ?'
        var data = {
            message: packet.payload.toString()
        }
        db.query(dbStat, data, (error, output) => {
            if(error){
                console.log(error)
            } else {
                console.log(output)
            }
        })
    }
});

server.on('ready', function(){
    console.log("Broker is ready!");
});