//
// main.js
//
// Scripts that should run on every page.
//

define(
    [
        'jquery',
        'underscore',

        'bootstrap'
    ], function ($, _) {

        /*
         * Global scripts
         */
        $(document).ready(function () {
            /*
             * Disable submit buttons on forms once they have been submitted once.
             */
            $('form').submit(function () {
                $(this).find('input[type="submit"]').attr('disabled', 'disabled');
            });

            /*
             * Collapse the collapsible sections
             */
            require(['jquery'], function () {
                // Slide up those sections not initially expanded
                $('.collapsible-section:not(.is-expanded) .collapsible-section-text').slideUp();

                // Prepare headers for clicking
                $('.collapsible-section-header').click(function () {
                    var $section = $(this).parent(),
                        $sectionText = $section.find('.collapsible-section-text');
                    $section.toggleClass('is-expanded');
                    $sectionText.slideToggle();
                });
            });

            /*
             * Fancy the fancyboxes
             */
            require(['jquery', 'fancybox'], function () {
                $('.fancybox').fancybox();
            });

            /*
             * If the tagline isn't fitting, squeeze it down.
             */
            var $tagline = $('.header-tagline');
            if ($tagline[0].scrollHeight > $tagline.innerHeight()) {
                $tagline.addClass('overflowing');
            }

            /*
             * If the navbar isn't fitting, squeeze it a bit. If it has room,
             * attempt to center it.
             */
            var $navbar = $('.navbar-default');
            if ($navbar[0].scrollHeight > $navbar.innerHeight()) {
                $navbar.addClass('overflowing');
            }
            else {
                var width = _.reduce(
                    $navbar.find('li'),
                    function (memo, e) { return memo + $(e).outerWidth(); },
                    0
                );
                $('.navbar-nav').outerWidth(width);
            }

        });


        /*
         * Page-specific modules
         */

        if ($('.map-page').length !== 0) {
            require(['mappage']);
        }

        if ($('.lot-detail-page').length !== 0) {
            require(['lotdetailpage']);
        }

});
