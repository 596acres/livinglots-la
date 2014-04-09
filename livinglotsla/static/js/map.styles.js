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

    function asCartocss(tableName) {
        var cartocss = '#' + tableName + ' {';

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
