$(function () {
    // Update number of likes when user clicks on 'like' button on an outfit
    $(".outfit-like-btn").click(function(){
        var pk = $(this).attr('id');
        var like = $(this).closest(".outfit-buttons").find(".num-outfit-likes");
        //TODO: make this to add 'true' or 'false' at the end of the url
        $.get(
            '/outfit/like/'+pk,
            function(responseText){
                like.html(responseText);
            },
            "html"
        );
    });

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


    // Function to display rest of outfit angles when hovered over on home page
    // these variables are not ideal, they are set in success which is used in the unhovered part of the function
    //TODO: figure out a better way to do this, setting global variables like swapImageFunc
    // makes the pictures on home page get swapped sometimes, and clear interval doesn't work all the time
    var primaryImage;
    var swapImageFunc;

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

                primaryImage = img.attr('src');
                data.push(primaryImage);

                swapImageFunc = setInterval(function() {
                    img.attr('src', data[i]);
                    i = (i+1) % data.length;
                }, 1000);
            }
        });
    };

    var outfitHoverOutFunc = function() {
        clearInterval(swapImageFunc);
        $(this).find('.preview-img').attr('src', primaryImage);
    };

    $(".photo-image").hoverIntent({
        over: outfitHoverInFunc,
        out: outfitHoverOutFunc,
        timeout: 400
    });
});
