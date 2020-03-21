/**
 * Handle main page Events.
 *
 * Manipulação dos eventos da página principal
 *
 * @version    1.0.0
 * @package    VocatioTelecom
 * @subpackage js
 * @author     Alcindo Schleder <alcindoschleder@gmail.com>
 *
 */

var IndexEvents = function () {

    var car_id = $('#car_id').val();
    var display_id = $('#display_id').val();

    var wsGroup = null
    var wsMember = null

    var set_display_controls = function (message) {
        console.log('setting display controls');
        if ((message == 'display_enable') && (!$('.shadow-page').hasClass('d-none')))
            $('.shadow-page').addClass('d-none');
        if ((message == 'display_disable') && ($('.shadow-page').hasClass('d-none')))
            $('.shadow-page').removeClass('d-none');
    }
    var checkCommands = function(e) {
        let data = JSON.parse(e.data);
        console.log('receiving: ', data);
        console.log('checking command:', data.command);
        console.log('checking message:', data.message);
        if (data.command == 'control')
            set_display_controls(data.message);
        if (data.command == 'setbox') {
            console.log('setting display box code');
            $('.box_code').html(data.message);
        }
    }
    var onCloseSocket = function (e) {
        console.error('Display socket closed unexpectedly', e);
    }
    var socketConnect = function(socket, url) {
        console.log('Connecting to:', url)
        socket = new WebSocket(url);
        socket.onmessage = checkCommands;
        socket.onclose = onCloseSocket;
    }
    var documentEvents = function () {
        socketConnect(wsGroup, 'ws://' + window.location.host + '/ws/car/' + car_id + '/')
        socketConnect(wsMember, 'ws://' + window.location.host + '/ws/display/' + car_id + '/' + display_id + '/')
        $('.btnTeste').on('click', (e) => {
            $('.shadow-page').removeClass('d-none');
        })
    };
    var handleDynamicLinks = function () {
    };
    var serializerJson = function(form) {
        let js = {};
        let a = $(form).serializeArray();
        $.each(a, function() {
           if (js[this.name]) {
               if (!js[this.name].push) {
                   js[this.name] = [js[this.name]];
               };
               js[this.name].push(this.value || '');
           } else {
               js[this.name] = this.value || '';
           };
       });
       return js;
    };
    var hidePage = function (page, url) {
    };
    var showPage = function (page, url) {
    };

    return {
        //main function to initiate the module
        init: function () {
            documentEvents();
        }
    };
}();

$(document).ready(function() {
    IndexEvents.init(); // starting home page events
});
