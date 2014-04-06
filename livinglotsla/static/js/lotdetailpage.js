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

            $('#file-modal').on('loaded.bs.modal', function () {
                modalForm('file-modal');
            });
            $('#note-modal').on('loaded.bs.modal', function () {
                modalForm('note-modal');
            });
            $('#organizer-modal').on('loaded.bs.modal', function () {
                modalForm('organizer-modal');
            });
            $('#photo-modal').on('loaded.bs.modal', function () {
                modalForm('photo-modal');
            });
            $('#steward-modal').on('loaded.bs.modal', function () {
                modalForm('steward-modal');
            });

            if (window.location.hash === '#organize') {
                $('#organizer-modal').modal({
                    show: true,
                    remote: $('.build-community-button').attr('href')
                });
            }
        });

    }
);
