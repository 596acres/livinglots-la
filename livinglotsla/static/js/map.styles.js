//
// Lot map styles by layer for maps
//

define(['underscore'], function (_) {

    var layers = {
        in_use: '#999933',
        private: '#CC99CC',
        private_tax_default: '#996699',
        private_ab_551: '#663366',
        public: '#990000',
        public_remnant: '#993333',
        public_sidelot: '#996666'
    };

    var defaults = {
        'marker-allow-overlap': 'true',
        'marker-fill': 'black',
        'marker-line-color': 'white',
        'marker-line-width': 1,
        'marker-width': 10
    };

    var burstFile = 'http://dev.laopenacres.org/static/img/burst.svg';

    var organizingColor = '#FF00FF';

    var organizingStyle = {
        'marker-allow-overlap': 'true',
        'marker-fill': organizingColor,
        // TODO make domain-agnostic? Using Django.js?
        'marker-file': 'url("' + burstFile + '")',
        'marker-width': 20
    };

    var friendlyOwnerColor = '#663300';

    var friendlyOwnerStyle = {
        'marker-allow-overlap': 'true',
        'marker-fill': friendlyOwnerColor,
        'marker-file': 'url("' + burstFile + '")',
        'marker-width': 20
    };

    function joinStyle(style) {
        return  _.reduce(_.keys(style), function (memo, property) {
            return memo + [property, style[property]].join(':') + ';';
        }, '');
    }

    function asCartocss(tableName) {
        var layerFills = _.reduce(_.keys(layers), function (memo, name) {
            return memo + '[layer = "' + name + '"] {' +
                'marker-fill: ' + layers[name] + ';' +
            '}';
        }, '');

        var markerStyle = joinStyle(defaults);

        var cartocss = '#' + tableName + ' {';

        // Default markers
        cartocss += layerFills;
        cartocss += markerStyle;


        /*
         * Stars for organizing and friendly-owner. Done as attachments so they
         * will be rendered on top of other markers.
         */

        // Add star around friendly owner sites
        cartocss += '[friendly_owner=true]::friendly_owner {';
        cartocss += joinStyle(friendlyOwnerStyle);
        cartocss += '}';

        // Re-add markers for organizing sites
        cartocss += '[friendly_owner=true]::dots {';
        cartocss += layerFills;
        cartocss += markerStyle;
        cartocss += '}';

        // Add star around organizing sites
        cartocss += '[organizing=true]::organizing {';
        cartocss += joinStyle(organizingStyle);
        cartocss += '}';

        // Re-add markers for organizing sites
        cartocss += '[organizing=true]::dots {';
        cartocss += layerFills;
        cartocss += markerStyle;
        cartocss += '}';

        cartocss += '}';
        return cartocss;
    }

    return (function () {
        return _.extend({}, layers, {
            asCartocss: asCartocss,
            friendlyOwnerColor: friendlyOwnerColor,
            organizingColor: organizingColor
        });
    })();

});
