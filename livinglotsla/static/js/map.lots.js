//
// map.lots.js
//
// Add a simple, standard method for adding the lots layer to L.Map.
//
//

define(
    [
        'jquery', 'leaflet', 'map.styles', 

        'leaflet.lotlayer'
    ], 

    function ($, L, mapstyles) {

        function layerStyle(layer) {
            var style = {
                color: mapstyles[layer],
                fillColor: mapstyles[layer],
                fillOpacity: 0.5,
                opacity: 0.5,
                weight: 1
            };
            if (!style.fillColor) {
                style.fillColor = '#000000';
            }
            return style;
        }

        var selectedLotStyle = {
                color: '#000',
                fillOpacity: 0.75,
                opacity: 1
            },
            defaultParams = { 
                layers: 'public,public_sidelot,private',
                parents_only: true
            },
            defaultLotLayerOptions = {
                style: function (feature) {
                    return layerStyle(feature.properties.layer);
                }
            };

        L.extend(L.Map.prototype, {

            /*
             * NB: This doesn't do any tiling, so it would be expensive to do 
             * for the entire map. Plan on setting parameters that restrict the
             * bbox of the lots if you use this.
             */
            addSimpleLotsLayer: function (overrideParams) {
                var map = this,
                    selectedLotPk = map.options.lotPk,
                    params = L.extend({}, defaultParams, overrideParams || {}); 

                if (selectedLotPk) {
                    params.lot_center = selectedLotPk;
                }

                var url = map.options.lotsurl + '?' + $.param(params);
                $.getJSON(url, function (data) {
                    var lotsLayer = L.geoJson(data, {
                        style: function (feature) {
                            var style = layerStyle(feature.properties.layer);
                            if (selectedLotPk && feature.id === selectedLotPk) {
                                L.extend(style, selectedLotStyle);
                            }
                            return style;
                        }
                    });
                    lotsLayer.addTo(map);
                });
            },

            /*
             * Add lot polygons in a more sophisticated way than with 
             * addSimpleLotsLayer(), using leaflet.lotlayer.
             */
            addTiledPolygonLotLayer: function (overrideParams,
                                               overrideLotLayerOptions,
                                               addToMap) {
                if (this.polygonsLayer) {
                    this.removeLayer(this.polygonsLayer);
                }
                var params = L.extend({}, defaultParams, overrideParams),
                    url = this.options.lotPolygonsUrl + '?' + $.param(params),
                    options = {
                        serverZooms: [16],
                        unique: function (feature) {
                            return feature.id;
                        }
                    },
                    layerOptions = L.extend({}, defaultLotLayerOptions,
                                            overrideLotLayerOptions);

                this.polygonsLayer = L.lotLayer(url, options, layerOptions);
                if (addToMap) {
                    this.polygonsLayer.addTo(this);
                }
            }

        });
    }
);
