requirejs.config({
    baseUrl: "/static/js",
    paths: {
        "bootstrap": "../bower_components/bootstrap/dist/js/bootstrap",
        "cartodb": "../bower_components/cartodb.js/dist/cartodb.noleaflet",
        "django": "djangojs/django",
        "fancybox": "../bower_components/fancybox/source/jquery.fancybox",
        "jquery": "../bower_components/jQuery/dist/jquery.min",
        "jquery.form": "../bower_components/jquery-form/jquery.form",
        "jquery.mousewheel": "../bower_components/perfect-scrollbar/src/jquery.mousewheel",
        "jquery.infinitescroll": "../bower_components/infinite-scroll/jquery.infinitescroll",
        "handlebars": "../bower_components/handlebars/handlebars",
        "leaflet": "../bower_components/leaflet/leaflet-src",
        "leaflet.bing": "../bower_components/leaflet-plugins/layer/tile/Bing",
        "leaflet.dataoptions": "../bower_components/leaflet.dataoptions/src/leaflet.dataoptions",
        "leaflet.hash": "../bower_components/leaflet-hash/leaflet-hash",
        "leaflet.loading": "../bower_components/leaflet.loading/src/Control.Loading",
        "leaflet.snogylop": "../bower_components/leaflet.snogylop/src/leaflet.snogylop",
        "leaflet.usermarker": "../bower_components/leaflet.usermarker/src/leaflet.usermarker",

        "livinglots.addlot": "../bower_components/livinglots-map/src/livinglots.addlot",
        "livinglots.addlot.window": "../bower_components/livinglots-map/src/templates/addlot/window",
        "livinglots.addlot.success": "../bower_components/livinglots-map/src/templates/addlot/success",
        "livinglots.addlot.failure": "../bower_components/livinglots-map/src/templates/addlot/failure",
        "livinglots.addlot.existspopup": "../bower_components/livinglots-map/src/templates/addlot/existspopup",

        "nouislider": "../bower_components/nouislider/jquery.nouislider",
        "perfect-scrollbar": "../bower_components/perfect-scrollbar/src/perfect-scrollbar",
        "requirejs": "../bower_components/requirejs",
        "select2": "../bower_components/select2/select2",
        "spin": "../bower_components/spin.js/spin",
        "text": "../bower_components/requirejs-text/text",
        "underscore": "../bower_components/underscore/underscore",

        // TileLayer.GeoJSON paths
        "communist": "../bower_components/leaflet-tilelayer-vector/lib/communist.min",
        "TileCache": "../bower_components/leaflet-tilelayer-vector/src/TileCache",
        "AbstractWorker": "../bower_components/leaflet-tilelayer-vector/src/AbstractWorker",
        "CommunistWorker": "../bower_components/leaflet-tilelayer-vector/src/CommunistWorker",
        "TileLayer.GeoJSON": "../bower_components/leaflet-tilelayer-vector/src/TileLayer.GeoJSON",
        "TileLayer.Overzoom": "../bower_components/leaflet-tilelayer-vector/src/TileLayer.Overzoom",
        "TileQueue": "../bower_components/leaflet-tilelayer-vector/src/TileQueue"
    },
    shim: {
        "bootstrap": ["jquery"],
        "cartodb": {
            "deps": ["jquery", "leaflet"]
        },
        "django": {
            "deps": ["jquery"],
            "exports": "Django"
        },
        "handlebars": {
            "exports": "Handlebars"
        },
        "jquery.infinitescroll": ["jquery"],
        "leaflet.bing": ["leaflet"],
        "leaflet.hash": ["leaflet"],
        "leaflet.usermarker": ["leaflet"],
        "perfect-scrollbar": ["jquery.mousewheel"],
        "underscore": {
            "exports": "_"
        }
    }
});

// Load the main app module to start the app
requirejs(["main"]);
