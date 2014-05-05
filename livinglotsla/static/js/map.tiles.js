//
// map.tiles.js
//
// Add a simple, standard method for adding the tiles layer to L.Map.
//

define(
    ['leaflet'], 

    function (L) {

        var attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>', 
            url = 'https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png';

        L.extend(L.Map.prototype, {
            addTileLayer: function (options) {
                var layerOptions = {
                    attribution: attribution,
                    maxZoom: 19,
                    mapboxId: this.options.mapboxId
                };
                L.extend(layerOptions, options || {});

                return L.tileLayer(url, layerOptions).addTo(this);
            }
        });
    }
);
