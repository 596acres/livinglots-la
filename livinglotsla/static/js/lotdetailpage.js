//
// lotdetailpage.js
//
// Scripts that only run on the lot detail page.
//

define(
    [
        'jquery',
        'handlebars',
        'leaflet',
        'streetview',
        'django',

        'leaflet.dataoptions',
        'map.lots',
        'map.tiles',
        'modalform'
    ], function ($, Handlebars, L, StreetView, Django) {

        $(document).ready(function () {
            var map = L.map('lot-detail-map');
            map.addTileLayer();
            map.addSimpleLotsLayer();
            StreetView.load_streetview(
                $('.lot-detail-streetview').data('lon'),
                $('.lot-detail-streetview').data('lat'),
                $('.lot-detail-streetview'),
                $('.lot-detail-streetview-error')
            );

            // Prepare all of the modals, which will have forms
            $('.modal').each(function () {
                $(this).on('loaded.bs.modal', function () {
                    $(this).modalForm({ reloadOnSuccess: true });
                });
            });

            if (window.location.hash === '#organize') {
                $('#organizer-modal').modal({
                    show: true,
                    remote: $('.build-community-button').attr('href')
                });
            }

            if (window.location.hash.indexOf('#photos') === 0) {
                $.fancybox.open($('.fancybox'));
                var hashArgs = window.location.hash.split('/');
                if (hashArgs.length > 1) {
                    var index = $('.fancybox').index($('#photo-' + hashArgs[1]));
                    if (index > 0) {
                        $.fancybox.jumpto(index);
                    }
                }
            }

            $('#btn-admin-toggle').click(function () {
                if ($('.btn-admin:visible:not(.btn-admin-always-visible)').length > 0 ||
                    $('.admin-only:visible').length > 0) {
                    $('.btn-admin:not(.btn-admin-always-visible),.admin-only').hide();
                }
                else {
                    $('.btn-admin,.admin-only').show();
                }
                return false;
            });
        });

    }
);
