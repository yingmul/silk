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
});
