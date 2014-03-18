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

        'jquery.form',
        'leaflet.dataoptions'
    ], function ($, Handlebars, L, mapstyles, StreetView, Django) {

        function addBaseLayer(map) {
            var baseLayer = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                key: map.options.apikey,
                styleId: map.options.styleid
            }).addTo(map);
        }

        function addLotsLayer(map) {
            var url = map.options.lotsurl + '?' + 
                $.param({ lot_center: map.options.lotPk });
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
                        if (feature.properties.pk === map.options.lotPk) {
                            style.color = '#000';
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

            $('#organizer-modal').on('loaded.bs.modal', function () {
                modalForm('organizer-modal');
            });
        });

    }
);
