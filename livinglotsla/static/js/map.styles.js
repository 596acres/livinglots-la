//
// Lot map styles by layer for maps
//

define(['underscore'], function (_) {

    var layers = {
        in_use: '#999933',
        private: '#663366',
        private_tax_default: '#996699',
        private_ab_551: '#CC99CC',
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

    var organizingColor = '#FF00FF';

    var organizingStyle = {
        'marker-fill': organizingColor,
        // TODO make domain-agnostic? Using Django.js?
        'marker-file': 'url("http://dev.laopenacres.org/static/img/organizing.svg")',
        'marker-width': 20
    }

    function joinStyle(style) {
        return  _.reduce(_.keys(style), function (memo, property) {
            return memo + [property, style[property]].join(':') + ';';
        }, '');
    }

    function asCartocss(tableName) {
        var cartocss = '#' + tableName + ' {';

        // TODO add star for friendly owner places, eg
        //  #lots[layer='private'][friendly_owner=true]::friendly-star {}

        // Add star around organizing sites
        cartocss += '[organizing=true]::organizing {';
        cartocss += joinStyle(organizingStyle);
        cartocss += '}';

        cartocss += joinStyle(defaults);

        cartocss += _.reduce(_.keys(layers), function (memo, name) {
            return memo + '[layer = "' + name + '"] {' +
                'marker-fill: ' + layers[name] + ';' +
            '}';
        }, '');

        cartocss += '}';
        return cartocss;
    }

    return (function () {
        return _.extend({}, layers, {
            asCartocss: asCartocss,
            organizingColor: organizingColor
        });
    })();

});
