$(function () {
    // this is to update the selected-img that's only within this preview section
    // e.g. clicking on piece 1's thumbnail will only update the piece 1's display picture on the preview page
    // this is not that good since it assumes DOM, it's easily breakable
    $('.preview-thumbnails').on("click", "img", function() {
        var clickedImg = $(this).attr('src');
        $(this).parent().parent().find('.selected-img').attr('src', clickedImg);
    });

    $('#sell_not_loggedin').click(function (e) {
        e.preventDefault();
        var nextUrl = $(this).data("url");
        $('#login_modal').load('/login/', function() {
            $(this).data('next', nextUrl);
            $(this).modal('show');
            resetLoginForm();
        });
        return false;
    });

});