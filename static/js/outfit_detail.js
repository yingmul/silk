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

    // below is for adding a comment
    var options = {
        success:    addComment,  // post-submit callback
        timeout:    3000,
        dataType:   'json',
        clearForm: true,          // clear all form fields after successful submit
        resetForm: true           // reset the form after successful submit
    };

    // bind form using 'ajaxForm'
    $('#outfit_comment').ajaxForm(options);

    // post-submit callback
    function addComment(responseJson, statusText, xhr, $form)  {
        $('#num_comments').text(responseJson['num_comments']);
        $('#existing_comments').append(
            '<div class="comment-line">' +
            '<div class="comment-name">' + responseJson['author'] + '</div>' +
            '<div>' + responseJson['comment'] + '</div></div>'
        )
    }
});
