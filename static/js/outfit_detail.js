$(function () {
    var swapImageFunc;
    var primaryImage;
    var pieceHoverInFunc = function() {
        primaryImage = $(this).find('.outfit-piece-picture').attr('src');
        var imageUrls = []
        $(this).find('.outfit-piece-picture-other').each(function() {
            imageUrls.push(this.src);
        });
        imageUrls.push(primaryImage);

        var i=0;
        var img = $(this).find('.outfit-piece-picture');
        swapImageFunc = setInterval(function() {
            img.attr('src', imageUrls[i]);
            i = (i+1) % imageUrls.length;
        }, 1000);
    };

    var pieceHoverOutFunc = function() {
        clearInterval(swapImageFunc);
        $(this).find('.outfit-piece-picture').attr('src', primaryImage);
    };

    $(".outfit-piece").hoverIntent({
        over: pieceHoverInFunc,
        out: pieceHoverOutFunc,
        timeout: 400
    });
});
