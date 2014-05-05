define(['jquery', 'spin', 'jquery.form'],
    function ($, Spinner) {

        $.fn.modalForm = function (reloadOnSuccess) {
            var $modal = $(this),
                id = $(this).attr('id');
            $(this).find('form').submit(function () {
                // Disable button and add a spinner
                var $button = $(this).find('.btn-primary');
                $button.prop('disabled', true);
                var spinner = new Spinner({
                    length: 8,
                    lines: 9
                }).spin($button[0]);

                // Submit form via AJAX
                $(this).ajaxSubmit({
                    target: '#' + id + ' .modal-content',
                    success: function () {
                        // Assume we got the form again and modalFormize it
                        $modal.modalForm();
                    }
                });
                return false;
            });
            $(this).find('.btn-close-modal').click(function () {
                location.reload(false);
            });

            // Reload page on <Esc> or <Enter> if successful
            if (reloadOnSuccess) {
                $('body').keyup(function (e) {
                    if ((e.keyCode === 27 || e.keyCode === 13)
                        && $('.btn-close-modal').length > 0) {
                        location.reload(false);
                    }
                });
            }
        }

    }
);
