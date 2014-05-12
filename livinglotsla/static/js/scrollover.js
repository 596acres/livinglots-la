//
// scrollover.js
//
// Scripts that only run in the scrollover area of the main map
//

define(
    [
        'jquery',
        'django',
        'spin'
    ], function ($, Django, Spinner) {

        var currentPage = 1;

        function showMore($button) {
            currentPage++;
            var url = Django.url('activity_list') + '?page=' + currentPage,
                spinner = new Spinner({
                    length: 8,
                    lines: 9
                }).spin($button[0]);
            $button.addClass('disabled');

            $.get(url)
                .done(function (content) {
                    spinner.stop();
                    $button.removeClass('disabled').before(content);
                })
                .fail(function () {
                    spinner.stop();
                    $button.before($('<div></div>').text('No more activities to load'));
                });
        }

        $(document).ready(function () {
            $('#map-scrollover-show-more').click(function () {
                showMore($(this));
                return false;
            });
        });

    }
);
