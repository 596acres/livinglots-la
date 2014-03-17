//
// Lot map styles by layer for maps
//

define(['underscore'], function (_) {

    var layers = {
        in_use: '#BAB974',
        private: '#D4A7D4',
        private_tax_default: '#9A649E',
        public: '#A9756D',
        public_remnant: '#8C474D'
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
