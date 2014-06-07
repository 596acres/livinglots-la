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
        'friendlyowners',

        'bootstrap',
        'jquery.infinitescroll',
        'jquery.mousewheel',
        'perfect-scrollbar',

        'leaflet.loading',
        'leaflet.lotmap',
        'livinglots.addlot',

        'nouislider',
        'select2',

        'map.search',
        'modalform',
        'scrollover'
    ], function (Django, $, Handlebars, _, L, Spinner, singleminded, friendlyowners) {

        var sizeMin = 0,
            sizeMax = 3;

        var nearbyCircle,
            nearbyCircleSize = 804.7, // meters in .5 miles
            nearbyCircleStyle = {
                color: '#d0d0d0',
                fill: false,
                opacity: 0.8
            };

        function urlDecode(str) {
            return decodeURIComponent(str.replace(/\+/g, '%20'));
        }

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
                public_owners: publicOwners.join(',')
            };

            var selectedSizeMin = $('.filter-size').val()[0];
            if (selectedSizeMin > sizeMin) {
                params.size_min = selectedSizeMin;
            }

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

            var councilDistrict = $('.map-filters-councildistricts:input').val();
            if (councilDistrict && councilDistrict !== '') {
                params.council_district = councilDistrict;
            }

            var neighborhoodCouncil = $('.map-filters-neighborhoodcouncils:input').val();
            if (neighborhoodCouncil && neighborhoodCouncil !== '') {
                params.neighborhood_council = neighborhoodCouncil;
            }

            var zoneClass = $('.map-filters-zoneclasses:input').val();
            if (zoneClass && zoneClass !== '') {
                params.zone_class = zoneClass;
            }

            if (options && options.bbox) {
                params.bbox = map.getBounds().toBBoxString();
            }

            params.search = $('#map-filters-search').val();
            if ($('#map-filters-search-nearby').is(':checked')) {
                var lat = $('#map-filters-search-lat').val(),
                    lng = $('#map-filters-search-lng').val();
                if (lat && lng) {
                    params.nearby_center = [lat, lng].join(',');
                }
            }

            return params;
        }

        function adjustContentHeight(map) {
            var headerHeight = $('header').outerHeight(),
                otherHeight = headerHeight + $('footer').outerHeight(),
                windowHeight = $(window).height(),
                mainContentHeight = windowHeight - otherHeight,
                handleHeight = $('#map-scrollover-handle').outerHeight(),
                scrolloverTop = headerHeight + mainContentHeight - handleHeight,
                scrolloverBottom = mainContentHeight;
            $('#map').height(mainContentHeight);
            $('#map-scrollover').css({
                'margin-top': scrolloverTop,
                'padding-bottom': scrolloverBottom
            });

            if (map) {
                map.invalidateSize();
            }
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
                    $('#map-download').data('lots-count', data['lots-count']);
                })
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

        function updateBoundary(map, urlName, label, type) {
            // Clear inputs for other boundaries
            if (type !== 'communityplanareas') {
                $('.map-filters-communityplanareas.select2-container').select2('val', '');
            }
            if (type !== 'councildistricts') {
                $('.map-filters-councildistricts.select2-container').select2('val', '');
            }
            if (type !== 'neighborhoodcouncils') {
                $('.map-filters-neighborhoodcouncils.select2-container').select2('val', '');
            }

            // Update boundaries to selected boundary
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

        function setFilters(params, map) {
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

            // Community Plan Area
            if (params.community_plan_area) {
                var area = urlDecode(params.community_plan_area);
                $('.map-filters-communityplanareas').select2('val', area);
                updateBoundary(map, 'communityplanarea_details_geojson', area,
                               $('.map-filters-communityplanareas').data('type'));
            }

            // Council District
            if (params.council_district) {
                var label = urlDecode(params.council_district);
                $('.map-filters-councildistricts').select2('val', label);
                updateBoundary(map, 'councildistrict_details_geojson', label,
                               $('.map-filters-councildistricts').data('type'));
            }

            // Neighborhood Council
            if (params.neighborhood_council) {
                var council = urlDecode(params.neighborhood_council);
                $('.map-filters-neighborhoodcouncils').select2('val', council);
                updateBoundary(map, 'neighborhoodcouncil_details_geojson', council,
                               $('.map-filters-neighborhoodcouncils').data('type'));
            }

            // Zoning
            if (params.zone_class) {
                $('.map-filters-zoneclasses').select2('val', urlDecode(params.zone_class));
            }

            // Size
            var size = [sizeMin, sizeMax];
            if (params.size_min) {
                size[0] = parseFloat(params.size_min);
            }
            if (params.size_max) {
                size[1] = parseFloat(params.size_max);
            }
            $('.filter-size').val(size);
            updateSizeLabels();

            // Search & nearby
            if (params.search !== '') {
                var search = urlDecode(params.search);
                $('#map-filters-search').val(search);
            }
            if (params.nearby_center && params.nearby_center !== '') {
                var latlng = params.nearby_center.split(',');
                $('#map-filters-search-nearby').prop('checked', true);
                $('#map-filters-search-lat').val(latlng[0]);
                $('#map-filters-search-lng').val(latlng[1]);
            }
        }

        function updateDisplayedLotsAndLinks(map) {
            var params = buildLotFilterParams(map);
            map.updateDisplayedLots(params);
            updateDetailsLink(map);
            updateExportLinks(map);
            updateLotCount(map);
        }

        function scrolloverCheckIn() {
            $('#map-scrollover-handle').toggleClass('in', $('body').scrollTop() > 0);
        }

        $(document).ready(function () {
            adjustContentHeight();

            $('.filter-size').noUiSlider({
                connect: true,
                margin: 0.05,
                range: {
                    min: sizeMin,
                    max: sizeMax
                },
                start: [sizeMin, sizeMax],
                step: 0.05
            });
            updateSizeLabels();
            $('.filter-size').on({
                set: updateSizeLabels,
                slide: updateSizeLabels
            });

            $('.map-filters-zoneclasses').select2();

            $('.map-filters-neighborhoodcouncils').select2();
            $('.map-filters-neighborhoodcouncils').change(function () {
                updateBoundary(map, 'neighborhoodcouncil_details_geojson',
                               $(this).val(), $(this).data('type'));
            });

            var map = L.lotMap('map', {

                onMouseOverFeature: function (feature) {
                },

                onMouseOutFeature: function (feature) {
                }

            });
            $(window).resize(_.debounce(function () {
                adjustContentHeight(map);   
            }, 250));

            var params;
            if (window.location.search.length) {
                params = deparam();
                setFilters(params, map);
            }

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
                    if (nearbyCircle) {
                        map.removeLayer(nearbyCircle);
                    }
                })
                .on('searchresultfound', function (e, result) {
                    var latlng = [result.latitude, result.longitude];
                    map.addUserLayer(latlng);
                    $('#map-filters-search-lat').val(result.latitude);
                    $('#map-filters-search-lng').val(result.longitude);

                    if ($('#map-filters-search-nearby').is(':checked')) {
                        nearbyCircle = L.circle(latlng,
                            nearbyCircleSize,
                            nearbyCircleStyle
                        ).addTo(map);
                    }
                    updateDisplayedLotsAndLinks(map);
                });

            $('.filter').change(function () {
                updateDisplayedLotsAndLinks(map);
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
                $('#map-sidebar-parent').toggleClass('expanded',
                    $('#map-filters-parent.expanded').length > 0
                );
                $('#map-sidebar-parent').perfectScrollbar('update');
            });

            $('.map-filters-councildistricts').select2();
            $('.map-filters-councildistricts').change(function () {
                updateBoundary(map, 'councildistrict_details_geojson',
                               $(this).val(), $(this).data('type'));
            });

            $('.map-filters-communityplanareas').select2();
            $('.map-filters-communityplanareas').change(function () {
                updateBoundary(map, 'communityplanarea_details_geojson',
                               $(this).val(), $(this).data('type'));
            });

            updateDetailsLink(map);
            updateExportLinks(map);

            $('#map-sidebar-parent').perfectScrollbar({
                includePadding: true,
                suppressScrollX: true
            });

            map.on('lotaddwindowchange', function () {
                $('#map-sidebar-parent').perfectScrollbar('update');
            });

            $('#admin-button-add-lot').click(function () {
                map.enterLotAddMode();
            });

            $('[data-toggle=tooltip]').tooltip();

            $('.export').click(function () {
                var lotsCount = $('#map-download').data('lots-count');
                if (lotsCount === 0) {
                    alert($('#map-download').data('too-few'));
                    return false;
                }
                if (lotsCount > 2500) {
                    alert($('#map-download').data('too-many'));
                    return false;
                }
            });

            // Prepare all of the modals, which will have forms
            $('#friendlyowner-modal').each(function () {
                $(this).on('loaded.bs.modal', function () {
                    friendlyowners.onload(map.getCenter());
                    $(this).modalForm({
                        onSuccess: function () {
                            friendlyowners.onload(map.getCenter());
                        }                
                    });
                });
            });

            $('#map-scrollover-handle').click(function () {
                if (!$(this).is('.in')) {
                    $('body').animate({ scrollTop: 200 }, 1000);
                }
                else {
                    $('body').animate({ scrollTop: 0 }, 1000);
                }
                $(this).toggleClass('in');
            });

            $(document).scroll(scrolloverCheckIn);
            scrolloverCheckIn();

        });

    }
);
