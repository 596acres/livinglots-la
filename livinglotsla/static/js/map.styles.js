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
        'marker-allow-overlap': true,
        'marker-fill': 'black',
        'marker-line-color': 'white',
        'marker-line-width': 1,
        'marker-width': 10
    };

    var organizingStyle = {
        'marker-fill': '#FF00FF',
        // TODO make domain-agnostic?
        'marker-file': 'url(http://dev.laopenacres.org/static/img/organizing.svg)'
    }

    function asCartocss(tableName) {
        var cartocss = '#' + tableName + ' {';

        // TODO add star for friendly owner places, eg
        //  #lots[layer='private'][friendly_owner=true]::friendly-star {}

        // Add star around organizing sites
        cartocss += '[organizing=true]::organizing {';
        _.each(_.keys(organizingStyle), function (property) {
            cartocss += property + ': ' + organizingStyle[property] + ';';
        });
        cartocss += '}';

        _.each(_.keys(defaults), function (property) {
            cartocss += property + ': ' + defaults[property] + ';';
        });

        _.each(_.keys(layers), function (layer) {
            cartocss += '[layer = "' + layer + '"] {' +
                'marker-fill: ' + layers[layer] + ';' +
                '}';
        });

        cartocss += '}';
        return cartocss;
    }

    return (function () {
        return _.extend({}, layers, { asCartocss: asCartocss });
    })();

});
