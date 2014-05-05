//
// friendlyowners.js
//
// Scripts that only run with the friendlyowners widget
//

define(
    [
        'jquery',
        'handlebars',
        'leaflet',
        'django',

        'leaflet.dataoptions',
        'map.lots',
        'map.tiles'
    ], function ($, Handlebars, L, StreetView, Django) {

        var parcelsLayer,
            selectedParcel;

        var parcelDefaultStyle = {
            color: '#2593c6',
            fillOpacity: 0,
            weight: 2.5
        };

        var parcelSelectStyle = {
            fillColor: '#EEC619',
            fillOpacity: 0.5
        };

        var parcelLayerOptions = {

            onEachFeature: function (feature, layer) {
                layer.on({
                    'click': function (event) {
                        var map = this._map,
                            layer = event.layer,
                            feature = event.target.feature;
                        if (selectedParcel && selectedParcel.id === feature.id) {
                            selectedParcel = null;
                            layer.setStyle(parcelDefaultStyle);
                            $('#id_parcels').val('');
                        }
                        else {
                            if (selectedParcel) {
                                selectedParcel.layer.setStyle(parcelDefaultStyle);
                            }
                            selectedParcel = {
                                id: feature.id,
                                address: feature.properties.address,
                                layer: layer
                            };
                            $('#id_parcels').val(feature.id);
                            layer.setStyle(parcelSelectStyle);
                            layer.bindPopup(feature.properties.address || 'unknown address').openPopup();
                        }
                    },

                    'mouseover': function (event) {
                        var layer = event.layer,
                            feature = event.target.feature;
                        $('.map-add-lot-current-parcel').text(feature.properties.address);
                    }
                });
            },

            style: function (feature) {
                return parcelDefaultStyle;
            }

        };

        function addParcelsLayer(map) {
            if (parcelsLayer) {
                map.removeLayer(parcelsLayer);
            }
            var url = map.options.parcelsUrl;

            var options = {
                layerFactory: L.geoJson,
                minZoom: 16,
                serverZooms: [16],
                unique: function (feature) {
                    return feature.id;
                }
            };

            var layerOptions = L.extend({}, parcelLayerOptions);
            parcelsLayer = new L.TileLayer.Vector(url, options, layerOptions);
            map.addLayer(parcelsLayer);
        }

        return {
            onload: function (latlng) {
                var mapId = 'friendlyowner-parcel-map';
                if ($('#' + mapId).length === 0) return;
                var map = L.map(mapId);
                map.setView(latlng, 18);
                map.addTileLayer({ minZoom: 16 });
                map.addTiledPolygonLotLayer({}, {}, true);
                addParcelsLayer(map);
            }
        }

    }
);
