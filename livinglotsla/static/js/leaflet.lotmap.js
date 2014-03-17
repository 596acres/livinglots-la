define(
    [
        'jquery',
        'django',
        'leaflet',
        'map.styles',
        'underscore',
        'handlebars',

        'cartodb',
        'leaflet.bing',
        'leaflet.dataoptions',
        'leaflet.hash',
        'leaflet.lotlayer',
        'leaflet.lotmarker',
        'leaflet.usermarker'
    ], function ($, Django, L, mapstyles, _, Handlebars) {

        var cartodb = window.cartodb;

        L.LotMap = L.Map.extend({

            boundariesLayer: null,
            centroidsLayer: null,
            polygonsLayer: null,
            lotLayerTransitionPoint: 15,
            previousZoom: null,
            userLayer: null,
            userLocationZoom: 16,

            addingCentroidsLayer: false,

            lotLayerOptions: {
                onEachFeature: function (feature, layer) {
                    layer.on({
                        'click': function (layer) {
                            var latlng = layer.latlng,
                                x = this._map.latLngToContainerPoint(latlng).x,
                                y = this._map.latLngToContainerPoint(latlng).y - 100,
                                point = this._map.containerPointToLatLng([x, y]);
                            this._map.createAndOpenPopup(this.feature.id, latlng);
                            return this._map.setView(point, this._map._zoom);
                        },
                        'mouseover': function (event) {
                            this._map.options.onMouseOverFeature(event.target.feature);
                        },
                        'mouseout': function (event) {
                            this._map.options.onMouseOutFeature(event.target.feature);
                        }
                    });
                },
                pointToLayer: function (feature, latlng) {
                    var options = {};
                    if (feature.properties.has_organizers) {
                        options.hasOrganizers = true;
                    }
                    return L.lotMarker(latlng, options);
                },
                style: function (feature) {
                    var style = {
                        fillColor: '#000000',
                        fillOpacity: 1,
                        stroke: 1,
                        color: '#E7DADF'
                    };
                    style.fillColor = mapstyles[feature.properties.layer];
                    if (!style.fillColor) {
                        style.fillColor = '#000000';
                    }
                    return style;
                },
                popupOptions: {
                    autoPan: false,
                    maxWidth: 250,
                    minWidth: 250,
                    offset: [0, 0]
                },
            },

            createAndOpenPopup: function (lotPk, latlng) {
                var map = this,
                    url = Django.url('lots:lot_detail_json', { pk: lotPk });
                $.getJSON(url, function (lotData) {
                    var source = $('#popup-template').html(),
                        template = Handlebars.compile(source);
                    var context = {
                        detailUrl: Django.url('lots:lot_detail', { pk: lotPk }),
                        feature: {
                            // Mimic the situation that will exist
                            // in L.Handlebars, where feature data is 
                            // loaded as one large GeoJSON file
                            properties: lotData
                        }
                    };
                    var popup = L.popup()
                        .setLatLng(latlng)
                        .setContent(template(context))
                        .openOn(map);
                });
            },

            initialize: function (id, options) {
                options.zoomControl = false;
                L.Map.prototype.initialize.call(this, id, options);
                this.addBaseLayer();
                this.addLotsLayer({});
                L.control.zoom().addTo(this);
                L.Control.loading().addTo(this);
                var hash = new L.Hash(this);

                this.boundariesLayer = L.geoJson(null, {
                    color: '#58595b',
                    fill: false
                }).addTo(this);

                this.on('zoomend', function () {
                    var currentZoom = this.getZoom();
                    if (this.previousZoom) {
                        // Switch to centroids
                        if (currentZoom <= this.lotLayerTransitionPoint && 
                            this.previousZoom > this.lotLayerTransitionPoint) {
                            this.fire('lotlayertransition', { details: false });
                        }
                        // Switch to polygons
                        else if (currentZoom > this.lotLayerTransitionPoint &&
                                 this.previousZoom <= this.lotLayerTransitionPoint) {
                            this.fire('lotlayertransition', { details: true });
                        }
                    }
                    else {
                        // Start with centroids
                        if (currentZoom <= this.lotLayerTransitionPoint) {
                            this.fire('lotlayertransition', { details: false });
                        }
                        // Start with polygons
                        else if (currentZoom > this.lotLayerTransitionPoint) {
                            this.fire('lotlayertransition', { details: true });
                        }
                    }
                    this.previousZoom = currentZoom;
                });
            },

            addBaseLayer: function () {
                this.cloudmade = L.tileLayer('http://{s}.tile.cloudmade.com/{key}/{styleId}/256/{z}/{x}/{y}.png', {
                    key: this.options.apikey,
                    styleId: this.options.styleid
                }).addTo(this);

                this.bing = new L.BingLayer('Ajio1n0EgmAAvT3zLndCpHrYR_LHJDgfDU6B0tV_1RClr7OFLzy4RnkLXlSdkJ_x');

                // TODO re-add layers control
                /*
                var baseLayers = {
                    streets: cloudmade,
                    satellite: bing
                };

                L.control.layers(baseLayers, {}, {
                    position: 'topleft'               
                }).addTo(this);
                */
            },

            addLotsLayer: function (params) {
                this.addPolygonsLayer(params);
                if (this.getZoom() <= this.lotLayerTransitionPoint) {
                    this.addCentroidsLayer(params);
                    if (this.centroidsLayer) {
                        this.addLayer(this.centroidsLayer);
                    }
                    this.removeLayer(this.polygonsLayer);
                }
                else {
                    if (this.centroidsLayer) {
                        this.removeLayer(this.centroidsLayer);
                    }
                    this.addLayer(this.polygonsLayer);
                }
            },

            addCentroidsLayer: function (params) {
                if (this.centroidsLayer || this.addingCentroidsLayer) {
                    return;
                }
                var map = this;
                map.addingCentroidsLayer = true;
                cartodb.createLayer(map, {
                    user_name: 'laopenacres',
                    type: 'cartodb',
                    sublayers: [{
                        cartocss: mapstyles.asCartocss('lots_production'),
                        interactivity: 'id',
                        sql: 'SELECT * FROM lots_production'
                    }]
                })
                .addTo(map)
                .done(function (layer) {
                    map.centroidsLayer = layer;
                    map.addingCentroidsLayer = false;

                    layer.getSubLayer(0).setInteraction(true);
                    layer.on('featureClick', function (e, latlng, pos, data, sublayerIndex) {
                        map.createAndOpenPopup(data.id, latlng);
                    });

                    // Update mouse cursor when over a feature
                    layer.on('featureOver', function () {
                        $('#' + map._container.id).css('cursor', 'pointer');
                    });
                    layer.on('featureOut', function () {
                        $('#' + map._container.id).css('cursor', 'grab');
                    });

                    map.addLayer(layer);
                });
            },

            addPolygonsLayer: function (params) {
                if (this.polygonsLayer) {
                    this.removeLayer(this.polygonsLayer);
                }
                var url = this.options.lotPolygonsUrl + '?' + $.param(params);

                var options = {
                    serverZooms: [16],
                    unique: function (feature) {
                        return feature.id;
                    }
                };

                var layerOptions = L.extend({}, this.lotLayerOptions);
                this.polygonsLayer = L.lotLayer(url, options, layerOptions);
            },

            updateDisplayedLots: function (params) {
                this.removeLayer(this.polygonsLayer);
                this.updateCentroidsSQL(params);
                this.addLotsLayer(params);
            },

            updateCentroidsSQL: function (params) {
                var sql = 'SELECT * FROM lots_production';
                var whereConditions = [];
                if (params.layers) {
                    var layers = params.layers.split(',');
                    layers = _.map(layers, function (l) { return "'" + l + "'"; });
                    whereConditions.push('layer IN (' + layers.join(',') + ')');
                }
                if (params.size_max) {
                    whereConditions.push('size <= ' + params.size_max);
                }
                if (params.size_min) {
                    whereConditions.push('size >= ' + params.size_min);
                }
                if (whereConditions.length) {
                    sql += ' WHERE ' + whereConditions.join(' AND ');
                }
                this.centroidsLayer.getSubLayer(0).setSQL(sql);
            },

            addUserLayer: function (latlng) {
                this.userLayer = L.userMarker(latlng, {
                    smallIcon: true,
                }).addTo(this);
                this.setView(latlng, this.userLocationZoom);
            },

            removeUserLayer: function () {
                if (this.userLayer) {
                    this.removeLayer(this.userLayer);
                }
            },

            removeBoundaries: function (data, options) {
                this.boundariesLayer.clearLayers();
            },

            updateBoundaries: function (data, options) {
                this.boundariesLayer.clearLayers();
                this.boundariesLayer.addData(data);
                if (options.zoomToBounds) {
                    this.fitBounds(this.boundariesLayer.getBounds());
                }
            }

        });

        L.lotMap = function (id, options) {
            return new L.LotMap(id, options);
        };

    }
);
