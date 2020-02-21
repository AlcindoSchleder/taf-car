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
        console.log('clearing interval....');
        clearInterval(Check);
        let url = 'http://localhost:8000/api/mqtt/check_changes/';
        let car_id = $('#car_id').val();
        let display_id = $('#display_id').val();
        let command = {
            'car_id': car_id,
            'display_id': display_id
        };
        console.log('send command to api....', command)
        $.ajax({
            type: "GET",
            url: url,
            data: command,
            dataType: 'json',
            success: function(d) {
                console.log('dados retornados da API', d);
                if d.length
                Check = executeInterval();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                console.log('erro....', msg);
            }
        });
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

$(window).on('load', function() {
    IndexEvents.init(); // starting home page events
});
