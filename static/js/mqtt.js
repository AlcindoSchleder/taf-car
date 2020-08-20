var MqttControl = function () {
    var mqtt;
    var reconnectTimeout = 2000;
    const HOST = '192.168.0.20';
    const PORT = 10883;
    const CLIENT_ID = 'TafCar0001';
    const USER = 'icity-iot';
    const PWD  = '90Am10@Mgr';

    var onConnectionLost = function (responseObject) {
         $('text-danger').html('ERROR: MQTT Connection lost');
        if (responseObject.errorCode !== 0) {
            $('text-danger').html('ERROR: ' + responseObject.errorMessage);
        }
    }
    var onMessageArrived = function (message) {
        $('text-danger').html('Topic: ' + message.destinationName + '  | ' + message.payloadString);
    }
    var disconnect = function () {
        client.disconnect();
        $('text-danger').html('MQTT Disconnected');
    }
    var connect = function() {
        console.log('Conectando ao host ' + HOST + ':' + PORT);
        // ws://HOST:PORT
        mqtt = new Paho.MQTT.Client(HOST, PORT, '', CLIENT_ID);
        mqtt.onConnectionLost = onConnectionLost;
        mqtt.onMessageArrived = onMessageArrived;
        let options = {
            timeout: 3,
            userName: USER,
            password: PWD,
            onFailure: function () {
                $('text-danger').html('ERROR: Connection to: ' + HOST + ' on port: ' + PORT + ' failed.');
            },
            onSuccess: function () {
                console.log('connected');
                sendMessage('', 'client connected')
            }
        }
        mqtt.connect(options)
        console.log('Mqtt Conectado: ' + HOST + ':' + PORT);
    }
    var sendMessage = function (display, command) {
        console.log('preparing to send a message:', command, ' to display:', display)
        let message = new Paho.MQTT.Message(command);
        topic = (display == '') ? 'taf/car0001' : 'taf/car0001/' + display;
        message.destinationName = 'taf/car0001/' + display; //'taf/car0001/e21' -> display position ex:e21
        console.log('Sendin Message to topic:', message.destinationName)
        mqtt.send(message);
        console.log('mensagem enviada')
    };
    return {
        //main function to initiate the module
        init: function () {
            connect();
        },
        manageDisplay: function (display, command) {
            sendMessage(display, command)
        }
    };
}();
