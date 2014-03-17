//
// mappage.js
//
// Scripts that only run on the map page.
//

define(
    [
        'django',
        'jquery',
        'handlebars',
        'underscore',
        'leaflet',
        'spin',
        'singleminded',

        'jquery.infinitescroll',

        'leaflet.loading',
        'leaflet.lotmap',

        'nouislider',
        'select2',

        'map.search'
    ], function (Django, $, Handlebars, _, L, Spinner, singleminded) {

        var sizeMax = 3;

        function buildLotFilterParams(map, options) {
            var layers = _.map($('.filter-layer:checked'), function (layer) {
                return $(layer).attr('name'); 
            });
            var publicOwners = _.map($('.filter-owner-public:checked'), function (ownerFilter) {
                return $(ownerFilter).data('ownerPk');
            });
            var params = {
                layers: layers.join(','),
                parents_only: true,
                projects: $('.filter-projects').val(),
                public_owners: publicOwners.join(','),
                size_min: $('.filter-size').val()[0]
            };

            // Only include maximum size if it's less than the maximum in the
            // range.
            var selectedSizeMax = $('.filter-size').val()[1];
            if (selectedSizeMax < sizeMax) {
                params.size_max = selectedSizeMax;
            }

            var communityPlanAreas = $('.map-filters-communityplanareas:input').val();
            if (communityPlanAreas && communityPlanAreas !== '') {
                params.community_plan_area = communityPlanAreas;
            }

            var councilDistrict = $('.map-filters-councildistricts').data('selected');
            if (councilDistrict && councilDistrict !== '') {
                params.council_district = councilDistrict;
            }

            var neighborhoodCouncil = $('.map-filters-neighborhoodcouncils:input').val();
            if (neighborhoodCouncil && neighborhoodCouncil !== '') {
                params.neighborhood_council = neighborhoodCouncil;
            }

            if (options && options.bbox) {
                params.bbox = map.getBounds().toBBoxString();
            }

            return params;
        }

        function maximizeMainContentHeight() {
            var otherHeight = $('header').outerHeight() + $('footer').outerHeight(),
                windowHeight = $(window).height(),
                mainContentHeight = windowHeight - otherHeight;
            $('#map').height(mainContentHeight);
        }

        function updateLotCount(map) {
            var url = Django.url('lots:lot_count') + '?' +
                $.param(buildLotFilterParams(map, { bbox: true }));
            singleminded.remember({
                name: 'updateLotCount',
                jqxhr: $.getJSON(url, function (data) {
                    _.each(data, function (value, key) {
                        $('#' + key).text(value);
                    });
                })
            });
        }

        function updateOwnershipOverview(map) {
            var url = Django.url('lots:lot_ownership_overview'),
                params = buildLotFilterParams(map, { bbox: true });
            $.getJSON(url + '?' + $.param(params), function (data) {
                var template = Handlebars.compile($('#details-template').html());
                var content = template({
                    lottypes: data
                });
                $('.details-overview').html(content);
            });
        }

        function updateDetailsLink(map) {
            var params = buildLotFilterParams(map);
            delete params.parents_only;

            var l = window.location,
                query = '?' + $.param(params),
                hash = L.Hash.formatHash(map),
                url = l.protocol + '//' + l.host + l.pathname + query + hash;
            $('a.details-link').attr('href', url);
        }

        function updateExportLinks(map) {
            var params = $.param(buildLotFilterParams(map, { bbox: true }));
            $('.export').each(function () {
                $(this).attr('href', $(this).data('baseurl') + params);
            });
        }

        function deparam() {
            var vars = {},
                param,
                params = window.location.search.slice(1).split('&');
            for(var i = 0; i < params.length; i++) {
                param = params[i].split('=');
                vars[param[0]] = decodeURIComponent(param[1]);
            }
            return vars;
        }

        function updateSizeLabels() {
            var range = $('.filter-size').val(),
                min = range[0],
                max = range[1];
            $('.filter-size-label-min').html(min + ' acres');

            if (max == sizeMax) {
                max = sizeMax + '+';
            }
            $('.filter-size-label-max').html(max + ' acres');
        }

        function updateBoundary(map, urlName, label) {
            if (label) {
                var url = Django.url(urlName, { label: label });
                $.getJSON(url, function (data) {
                    map.updateBoundaries(data, { zoomToBounds: true });
                });
            }
            else {
                map.removeBoundaries();
            }
        }

        function setFilters(params) {
            // Clear checkbox filters
            $('.filter[type=checkbox]').prop('checked', false);

            // Set layers filters
            var layers = params.layers.split(',');
            _.each(layers, function (layer) {
                $('.filter-layer[name=' + layer +']').prop('checked', true);
            });

            // Set owners filters
            var publicOwners = params.public_owners.split(',');
            _.each(publicOwners, function (pk) {
                $('.filter-owner-public[data-owner-pk=' + pk +']').prop('checked', true);
            });

            // Set boundaries filters

            var projects = params.projects;
            if (projects !== '') {
                $('.filter-projects').val(projects);
            }
        }

        $(window).resize(_.debounce(maximizeMainContentHeight, 250));

        $(document).ready(function () {
            maximizeMainContentHeight();

            var params;
            if (window.location.search.length) {
                params = deparam();
                setFilters(params);
            }

            var map = L.lotMap('map', {

                onMouseOverFeature: function (feature) {
                },

                onMouseOutFeature: function (feature) {
                }

            });

            map.addLotsLayer(buildLotFilterParams(map));

            $('.details-print').click(function () {
                // TODO This is not a good solution since the map size changes
                // on print. Look into taking screenshots like:
                //   https://github.com/tegansnyder/Leaflet-Save-Map-to-PNG
                //   http://html2canvas.hertzen.com
                window.print();
            });

            $('form.map-filters-search-form').mapsearch()
                .on('searchstart', function (e) {
                    map.removeUserLayer();
                })
                .on('searchresultfound', function (e, result) {
                    map.addUserLayer([result.latitude, result.longitude]);
                });

            $('.filter').change(function () {
                var params = buildLotFilterParams(map);
                map.updateDisplayedLots(params);
                updateDetailsLink(map);
                updateExportLinks(map);
                updateLotCount(map);
            });

            $('.map-filters-type-item').click(function () {
                $(this).toggleClass('on');
                var $input = $(this).find(':input');
                $input
                    .prop('checked', function (i, val) {
                        return !val;
                    })
                    .trigger('change');
            });

            updateLotCount(map);
            map.on({
                'moveend': function () {
                    updateDetailsLink(map);
                    updateExportLinks(map);
                    updateLotCount(map);
                },
                'zoomend': function () {
                    updateDetailsLink(map);
                    updateExportLinks(map);
                    updateLotCount(map);
                },
                'lotlayertransition': function (e) {
                    map.addLotsLayer(buildLotFilterParams(map));
                }
            });

            $('.map-filters-expander').click(function () {
                $(this).parent('.map-filters').toggleClass('expanded');
            });

            $('.map-filters-councildistrict').click(function () {
                var label = $(this).data('label');
                updateBoundary(map, 'councildistrict_details_geojson', label);
                $('.map-filters-councildistricts').data('selected', label);
                return false;
            });

            $('.map-filters-communityplanareas').select2();
            $('.map-filters-communityplanareas').click(function () {
                // TODO actually update filters
                updateBoundary(map, 'communityplanarea_details_geojson',
                               $(this).val());
                return false;
            });

            $('.map-filters-neighborhoodcouncils').select2();
            $('.map-filters-neighborhoodcouncils').change(function () {
                // TODO actually update filters
                updateBoundary(map, 'neighborhoodcouncil_details_geojson',
                               $(this).val());
                return false;
            });

            $('.filter-size').noUiSlider({
                connect: true,
                margin: 0.05,
                range: {
                    min: 0,
                    max: sizeMax
                },
                start: [0, sizeMax],
                step: 0.05
            });
            updateSizeLabels();
            $('.filter-size').on({
                set: updateSizeLabels,
                slide: updateSizeLabels
            });

            updateDetailsLink(map);
            updateExportLinks(map);

        });

    }
);
