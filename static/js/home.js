$(function () {
    // Update number of likes when user clicks on 'like' button on an outfit
    $(".home-btn-like").click(function(){
        var $this = $(this),
            pk = $(this).attr('id'),
            like = $(this).closest(".home-outfit-buttons").find(".num-outfit-likes"),
            likeness = !($this.hasClass('active'));

        $.get(
            '/outfit/like/'+pk+'/'+likeness,
            function(responseText){
                $this.toggleClass('active');
                if (likeness) {
                    like.html(responseText);
                }
            },
            "html"
        );
    });

    // Function to display rest of outfit angles when hovered over on home page
    var outfitHoverInFunc = function() {
        $.ajax({
            context: this,
            type: 'GET',
            url: '/outfit/pictures/'+$(this).attr('id'),
            beforeSend:function(){
                // display the spinner and make image opaque when loading the rest of the images
                $(this).find('.loading-img').css( 'display', 'block' );
                $(this).find('.preview-img').css( 'opacity', '0.4');
            },
            success: function(data) {
                $(this).find('.loading-img').css( 'display', 'none' );
                $(this).find('.preview-img').css( 'opacity', '1.0');
                var img = $(this).find('.preview-img');
                var i = 0;

                var primaryImage = img.attr('src');
                data.push(primaryImage);

                var swapImageFunc = setInterval(function() {
                    img.attr('src', data[i]);
                    i = (i+1) % data.length;
                }, 1000);

                // use $(this).data, so no need to declare primaryImage or swapImageFunc as
                // a global variable, otherwise race condition occur
                $(this).data('primaryImage', primaryImage);
                $(this).data('timeout', swapImageFunc);
            }
        });
    };

    var outfitHoverOutFunc = function() {
        clearInterval($(this).data('timeout'));
        $(this).find('.preview-img')
            .attr(
                'src',
                $(this).data('primaryImage')
            );
    };

    $(".photo-image").hoverIntent({
        over: outfitHoverInFunc,
        out: outfitHoverOutFunc,
        timeout: 400
    });

    $('#feedbackModal').on('show', function() {
        $(this).find('.feedback-form').css( 'display', 'block');
        $(this).find('.feedback-received').css( 'display', 'none' );
        $(this).find("textarea").val("");
    });

    $('#feedbackModal').on('submit', '#feedback_form', function(e) {
        e.preventDefault();
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            beforeSend:function(){
                $(this).find('.feedback-form').css( 'display', 'none');
                $(this).find('.feedback-received').css( 'display', 'block' );
            },
            success: function(data, status) {
                // close the modal and reload the current page
                $('#feedbackModal').modal('hide');
            }
        });
    });

});
