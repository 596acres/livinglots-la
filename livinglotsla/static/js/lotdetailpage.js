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
        'map.styles',
        'streetview',
        'django',

        'leaflet.dataoptions',
        'modalform'
    ], function ($, Handlebars, L, mapstyles, StreetView, Django) {

        function addBaseLayer(map) {
            L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
                maxZoom: 18,
                mapboxId: map.options.mapboxId
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
