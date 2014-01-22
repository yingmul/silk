$(function () {
    $('.piece-thumbnails').on("click", "img", function() {
        var clickedImg = $(this).attr('src');
        $('.piece-selected-img').attr('src', clickedImg);
    });

    var options = {
        success:    addComment,  // post-submit callback
        timeout:    3000,
        dataType:   'json',
        clearForm: true,          // clear all form fields after successful submit
        resetForm: true           // reset the form after successful submit
    };

    // bind form using 'ajaxForm'
    $('#piece_comment').ajaxForm(options);

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
