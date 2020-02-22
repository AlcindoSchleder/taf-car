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
    var Check = null;
    var executeInterval = function () {
        return setInterval(function() {
            checkChanges();
        }, 5000);
    }
    var documentEvents = function () {
        Check = executeInterval();
    };
    var checkChanges = function () {
        clearInterval(Check);
        let url = 'http://192.168.0.203/api/mqtt/check_changes/';
//        let url = 'http://192.168.0.13:8000/api/mqtt/check_changes/';
        let car_id = $('#car_id').val();
        let display_id = $('#display_id').val();
        let command = {
            'car_id': car_id,
            'display_id': display_id
        };
        $.ajax({
            type: "GET",
            url: url,
            data: command,
            dataType: 'json',
            success: function(msg) {
                if ((msg.data) && (msg.data.length > 0))
                    checkCommands(msg.data);
                Check = executeInterval();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                console.log('erro....', msg);
            }
        });
    };
    var checkCommands = function(data_array) {
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

$(window).on('load', function() {
    IndexEvents.init(); // starting home page events
});
