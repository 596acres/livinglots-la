//
// mappage.js
//
// Scripts that only run on the map page.
//

define(
    [
        'jquery',
        'handlebars',
        'leaflet',
        'map.styles',
        'streetview',
        'django',
        'spin',

        'jquery.form',
        'leaflet.dataoptions'
    ], function ($, Handlebars, L, mapstyles, StreetView, Django, Spinner) {

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map) {
            var url = map.options.lotsurl + '?' + 
                $.param({ 
                    layers: 'public,public_sidelot,private',
                    lot_center: map.options.lotPk,
                    parents_only: true
                });
            $.getJSON(url, function (data) {
                var lotsLayer = L.geoJson(data, {
                    style: function (feature) {
                        var style = {
                            color: mapstyles[feature.properties.layer],
                            fillColor: mapstyles[feature.properties.layer],
                            fillOpacity: 0.5,
                            opacity: 0.5,
                            weight: 1
                        };
                        if (feature.id === map.options.lotPk) {
                            style.color = '#000';
                            style.fillOpacity = 0.75;
                            style.opacity = 1;
                        }
                        return style;
                    }
                });
                lotsLayer.addTo(map);
            });
        }

        function modalForm(modalId) {
            $('#' + modalId).find('form').submit(function () {
                // Disable button and add a spinner
                var $button = $(this).find('.btn-primary');
                $button.prop('disabled', true);
                var spinner = new Spinner({
                    length: 8,
                    lines: 9
                }).spin($button[0]);

                // Submit form via AJAX
                $(this).ajaxSubmit({
                    target: '#' + modalId + ' .modal-content',
                    success: function () {
                        modalForm(modalId);
                    }
                });
                return false;
            });
            $('#' + modalId).find('.btn-close-modal').click(function () {
                location.reload(false);
            });

            // Reload page on <Esc> or <Enter> if successful
            $('body').keyup(function (e) {
                if ((e.keyCode === 27 || e.keyCode === 13) && $('.btn-close-modal').length > 0) {
                    location.reload(false);
                }
            });
        }

        $(document).ready(function () {
            var map = L.map('lot-detail-map');
            addBaseLayer(map);
            addLotsLayer(map);
            StreetView.load_streetview(
                $('.lot-detail-streetview').data('lon'),
                $('.lot-detail-streetview').data('lat'),
                $('.lot-detail-streetview'),
                $('.lot-detail-streetview-error')
            );

            // Prepare all of the modals, which will have forms
            $('.modal').each(function () {
                $(this).on('loaded.bs.modal', function () {
                    modalForm($(this).attr('id'));
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
