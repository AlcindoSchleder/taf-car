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
    const ERROR = 1;
    const SUCCESS = 2;
    const MAP_COLOR = {
        1: 'text-danger',
        2: 'text-success'
    }

    var documentEvents = function () {
        $('#form_boxes input').on('keypress', function (e) {
            let keycode = (e.keyCode ? e.keyCode : e.which);
            if (keycode == '13')
                var inputs = $(this).parents("form").eq(0).find(":input");
                var idx = inputs.index(this);

                if (idx == inputs.length - 1) {
                    $('#form_boxes').submit() // validate and save form
                } else {
                    inputs[idx + 1].focus();
                    inputs[idx + 1].select();
                }
                return false;
        });
        $('#form_boxes input').focusin(function (e) {
            let display = $(this).attr('name');
            let carid = $('.carid').html()
            manageDisplay(carid, display, 'display_enable');
        });
        $('#form_boxes input').focusout(function (e) {
            let display = $(this).attr('name');
            let value = $(this).val();
            let carid = $('.carid').html()
            manageDisplay(carid, display, 'setbox');
            manageDisplay(carid, display, 'display_disable');
        });
        $('#e21').focus();
        $('#e21').select();
    };
    var manageDisplay = function (carid, display, message) {
//        let url = 'http://192.168.0.203/api/mqtt/send_message/'
        let url = 'http://localhost:8000/api/mqtt/send_message/';
        let command = {
            'type': 'control',
            'carid': carid,
            'display': display,
            'message': message
        };
        $.ajax({
            type: "GET",
            url: url,
            data: command,
            dataType: 'json',
            success: function(d) {
//                d = JSON.parse(d);
                console.log(d)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                console.log('erro....', msg);
            }
        });
    };
    var handleDynamicLinks = function () {
        $('.main-nav li a, .servicelink').bind('click', function(event) {
            var $anchor = $(this);

            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 102
            }, 1500, 'easeInOutExpo');
            /*
            if you don't want to use the easing effects:
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top
            }, 1000);
            */
            if ($(window).width() < 768) {
                $('.main-nav').hide();
            }
            event.preventDefault();
        });
        $('#form-test-api, #form-get-token').on('submit', function(e) {
            e.preventDefault();
            dataKey = $(this).attr('data-key');
            IndexEvents.formSubmitEvent(dataKey);
        });
    };
    var serializerJson = function(form) {
        let js = {}
        let a = $(form).serializeArray()
        $.each(a, function() {
           if (js[this.name]) {
               if (!js[this.name].push) {
                   js[this.name] = [js[this.name]];
               }
               js[this.name].push(this.value || '');
           } else {
               js[this.name] = this.value || '';
           }
       });
       return js;
    };
    var clearForm = function (form) {
        $(form).find('input[type=text],input[type=email]').val('');
    }
    var getTokenToTest = function () {
        data = serializerJson('#form-get-token');
        if ((!data['g-recaptcha-response']) ||
            (data['g-recaptcha-response'] == "") ||
            (data['g-recaptcha-response'] == undefined) ||
            (data['g-recaptcha-response'] == 0)) {
            $('#captcha-help').html('Você deve marcar este campo...');
            return false;
        }
        let url = data['host-url'] + "/api/home/gen_test_token/";
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function(d) {
                d = JSON.parse(d);
                configureSearchTax();
                $('#token-access').val(d.token);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                IndexEvents.showMessageIn('#form-test-api-help', msg, ERROR);
                console.log('erro....', msg);
            },
            dataType: "json"
        });
    };
    var getQueryTax = function () {
    }
    var gotoTop = function () {
    };
    var showPage = function (page, url) {
    };

    return {
        //main function to initiate the module
        init: function () {
            documentEvents();
        },
        formSubmitEvent: function () {
        }
    };
}();

$(window).on('load', function() {
    IndexEvents.init(); // starting home page events
});
