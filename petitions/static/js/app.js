;(function ($) {

    $(document).ready(function ready() {
        // Put > in front of each link in site switcher
        $('<i class="icon icon-angle-right"></i>').insertBefore('ul.siteswitcher li > a');
    });

    // Siteswitcher on hover, make opacity 1, otherwise fade back to 0.3.
    $('#siteswitcher').css('opacity', 0.3);
    $('#siteswitcher').hover(function hover_siteswitcher() {
        $(this).animate({opacity: 1});
    }, function onhoverleave_siteswitcher() {
        $('#siteswitcher .sites').delay(3000).hide(0);
        $(this).delay(3000).animate({opacity: 0.3});
    });

    // On click of the site switcher, toggle sites div visible.
    $('#siteswitcher .btn').on('click', function click_siteswitcher(evt) {
        evt.preventDefault();
        $('#siteswitcher .sites').toggle();
        var selector = '#siteswitcher .btn i';
        if ($(selector).hasClass('fa-angle-down')) {
            $(selector).removeClass('fa-angle-down').addClass('fa-angle-up');
        } else {
            $(selector).removeClass('fa-angle-up').addClass('fa-angle-down');
        }
        return false;
    });

}(jQuery));
