;(function ($) {

    $(document).ready(function ready() {
        // Put > in front of each link in site switcher
        $('<i class="icon icon-angle-right"></i>').insertBefore('ul.siteswitcher li > a');
    });

    // Siteswitcher and languages on hover, make opacity 1, otherwise fade back
    // to 0.3.
    $('#siteswitcher, ul.languages').css('opacity', 0.3);
    $('#siteswitcher').hover(function hover_siteswitcher() {
        $(this).animate({opacity: 1});
    }, function onhoverleave_siteswitcher() {
        $('#siteswitcher .sites').delay(3000).hide(0);
        $(this).delay(3000).animate({opacity: 0.3});
    });
    $('ul.languages').hover(function hover_languages() {
        $(this).animate({opacity: 1});
    }, function onhoverleave_languages() {
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

    // Language switcher logic
    $('ul.languages > li > a').on('click', function click_language(evt) {
        evt.preventDefault();
        var language_clicked = $(this).data('languageCode');
        $('form#language_form select').val(language_clicked);
        $('form#language_form').submit();
        return false;
    });

}(jQuery));
