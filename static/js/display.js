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

    var display_id = "{{ display_id|escapejs }}";

    var documentEvents = function () {

        var chatSocket = new WebSocket(
            'ws://' + window.location.host +
            '/ws/display/' + display_id + '/'
        );

        chatSocket.onmessage = checkCommands;
        chatSocket.onclose = function(e) {
            console.error('Display socket closed unexpectedly');
        };
    };
    var checkCommands = function(e) {
        let data_array = JSON.parse(e.data);
        for (let i = 0; i < data_array.length; i++) {
            if (data_array[i].box_type_command == 'control')
                set_display_controls(data_array[i].box_message);
            if (data_array[i].box_type_command == 'setbox')
                $('.box_code').html(data_array[i].box_message);
        };
    }
    var set_display_controls = function (message) {
        if ((message == 'display_enable') && (!$('.shadow-page').hasClass('d-none')))
            $('.shadow-page').addClass('d-none');
        if ((message == 'display_disable') && ($('.shadow-page').hasClass('d-none')))
            $('.shadow-page').removeClass('d-none');
    }
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
