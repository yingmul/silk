$(function () {
    $('.btn-counter').click(function() {
        var $this = $(this),
            count = $this.attr('data-count'),
            pk = $(this).attr('id'),
            likeness = !($this.hasClass('active'));

        $.get(
            '/outfit/like/'+pk+'/'+likeness,
            function(responseText){
                $this.toggleClass('active');
                $this.attr('data-count', responseText);

                if (likeness) {
                    $('.like-empty-heart').css('display', 'none');
                    $('.like-heart').css('display', 'inline');
                } else {
                    $('.like-heart').css('display', 'none');
                    $('.like-empty-heart').css('display', 'inline');
                }
            },
            "html"
        );
    })

    $('.outfit-thumbnails').on("click", "img", function() {
        var clickedImg = $(this).attr('src');
        $('.selected-img').attr('src', clickedImg);
    });

    var pieceHoverInFunc = function() {
        var primaryImage = $(this).find('.outfit-piece-picture').attr('src');
        var imageUrls = []
        $(this).find('.outfit-piece-picture-other').each(function() {
            imageUrls.push(this.src);
        });
        imageUrls.push(primaryImage);

        var i=0;
        var img = $(this).find('.outfit-piece-picture');
        var swapImageFunc = setInterval(function() {
            img.attr('src', imageUrls[i]);
            i = (i+1) % imageUrls.length;
        }, 1000);
         // use $(this).data, so no need to declare primaryImage or swapImageFunc as
        // a global variable, otherwise race condition occur
        $(this).data('primaryImage', primaryImage);
        $(this).data('timeout', swapImageFunc);
    };

    var pieceHoverOutFunc = function() {
        clearInterval($(this).data('timeout'));
        $(this).find('.outfit-piece-picture')
            .attr(
                'src',
                $(this).data('primaryImage')
            );
    };

    $(".outfit-piece").hoverIntent({
        over: pieceHoverInFunc,
        out: pieceHoverOutFunc,
        timeout: 400
    });

    // below is for adding a comment
    var options = {
        success:    addComment,  // post-submit callback
        error:      errorComment,
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

    function errorComment(jqXHR, exception) {
        if (jqXHR.status == 401) {
            // user is not logged in
            $('#login_modal').load('/login/', function() {
               $(this).modal('show');
            });
        }
    }
});
