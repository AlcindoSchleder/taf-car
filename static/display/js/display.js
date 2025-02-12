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

    var documentEvents = function () {
        wow = new WOW({
            animateClass: 'animated',
            offset: 100
        });
        wow.init();
        $(document).on('scroll', function () {
            if ($(window).scrollTop() > 100) {
                $('.scroll-top-wrapper').addClass('show');
            } else {
                $('.scroll-top-wrapper').removeClass('show');
            }
        });
        $('.res-nav_click').click(function() {
            $('.main-nav').slideToggle();
            return false
        });
        $('.serviceLink').scrollToFixed();
        $('#taxesModal').on('hidden.bs.modal', function (e) {
            location.reload();
        })
    };
    var onEditkeyPress = function () {
        $('body').bind('keyup', function(e) {
            if (e.KeyCode != #13) {
                chr += String.fromCharCode(e.keyCode).toLowerCase();
                console.log(chr);
                $('input:hidden').val(chr);
            } else {
                $('input:hidden').val('');
                checkProductCode($('input:hidden').val());
            }
        });
            // verify if product is correct and if not display alarm on screen and beep error
            // decrement counter of product
            // decrement counter of total products
            // form action:
               // hide empresa, codcarga, rua, prédio, local, cod_prod, cod_box, qtd_prod
               // input text display none bar_code
    };
    var checkProductCode = function(product_barcode) {
        if (!product_barcode) return False;
        data = serializerJson('#form_product_hidden');
        let url = "http://192.168.0.203:5180/tafApi/check_product/" + product_barcode;
        let result = {};
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function(d) {
                result = JSON.parse(d);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let msg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                IndexEvents.showMessageIn('#form_product_hidden', msg, ERROR);
                console.log('erro....', msg);
            },
            dataType: "json"
        });
        return ((result) && (result['state']) && (result['state']['Sttcode']) && (result['state']['Sttcode'] == 200));
    };
    var showSearchTax = function () {
        $('.test-taxes-api-token').fadeOut('slow', function () {
            $(this).addClass('d-none');
            $('.test-taxes-api-search').removeClass('d-none').fadeIn('slow', clearForm(this));
        });
    }
    var clearForm = function (form) {
        $(form).find('input[type=text],input[type=email]').val('');
    }
    var hideSearchTax = function () {
        $('.test-taxes-api-search').fadeOut('slow', function () {
            $(this).addClass('d-none');
            initRecaptcha();
            $('.test-taxes-api-token').removeClass('d-none').fadeIn('slow', clearForm(this));
        });
    }
    var configureSearchTax = function (show=true) {
        if (show) {
            showSearchTax();
        } else {
            hideSearchTax();
        }
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
        data = serializerJson('#form-test-api');
        token = data['token-access'];
        data['token-access'] = null;
        let url = data['host-url'] + "/api/home/query_tax/";
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            headers: {
                "Authorization": "token " + token
            },
            success: function(d) {
                if (typeof(d) == 'string'){
                    d = JSON.parse(d);
                };
                fillModalScreen(d);
                $('#taxesModal').modal('show');
                configureSearchTax(show=false);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                let errMsg = 'Um erro ocorreu ao chamar a API: status(' + textStatus + ') erro( ' + errorThrown + ')';
                configureSearchTax(show=false);
                IndexEvents.showMessageIn('#form-get-token-help', errMsg, ERROR);
                console.log('erro....', errMsg);
            },
            dataType: "json"
        });
    }
    var fillModalScreen = function (data) {
        $('.msg').html(data.message == 'OK' ? 'Produto Encontrado!' : 'Produto Não Encontrado!');
        $('.ncmCategory').html(data.category);
        $('.ncmProduct').html(data.product_NCM);
        $('.ncmUnity').html(data.unit);
        $('.ncmOrigin').html(data.from);
        $('.ncmDestiny').html(data.to);
        $('.tbTaxes .tbbody').html('');
        idx = 1;
        data.taxes.forEach(function (tax) {
            $(".tbTaxes .tbbody").append(
                "<div class='row " + idx +  "'>" +
                    "<div class='type_tax col-6'>" + tax.type_tax + "</div>" +
                    "<div class='tax col-6'>" + tax.tax + "% </div>" +
                "</div>"
            );
            idx += 1
        });
    }
    var gotoTop = function () {
        var T = $('body').offset.top;
        $('html, body').animate({scrollTop: 0}, 900, 'linear');
    };
    var autoScrollEvent = function () {
        $('.scroll-top-wrapper').on('click', function () {
            IndexEvents.scrollToTop();
        });
    };
    var showPage = function (page, url) {
    };

    return {
        //main function to initiate the module
        init: function () {
            documentEvents();
            autoScrollEvent();
            handleDynamicLinks();
        },
        scrollToTop: function () {
            gotoTop();
        },
        showMessageIn: function (element, msg, typeMsg = 0) {
            $(element).removeClass();
            if ((typeMsg > 0) && (typeMsg < 3)){
                $(element).addClass(MAP_COLOR[typeMsg]);
            } else {
                $(element).addClass('text-muted');
            };
            $(element).html(msg);
            setTimeout(function() {
                $(element).html('');
            }, 5000)
        },
        formSubmitEvent: function (formKey) {
            switch(formKey) {
                case 'get_test_token':
                    getTokenToTest();
                    break;
                case 'get_ncm_tax':
                    getQueryTax();
                    break;
                default:
                    console.log('Default case... nothing happen!!!');
            }
        }
    };
}();

$(window).on('load', function() {
    IndexEvents.init(); // starting home page events
});
