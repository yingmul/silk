$(function () {

    // Update number of likes when user clicks on 'like' button on an outfit
    $(".outfit-like-btn").click(function(){
        var pk = $(this).attr('id');
        var like = $(this).closest(".outfit-buttons").find(".num-outfit-likes");
        $.get(
            '/outfit/like/'+pk,
            function(responseText){
                like.html(responseText);
            },
            "html"
        );
    });

    $(document).on("click", ".outfit-modal", function () {
        var pk = $(this).data('id');


        $(".modal-body #bookId").val( pk );
    });


    // Function to display rest of outfit angles when hovered over on home page
    // these variables are not ideal, they are set in success which is used in the unhovered part of the function
    var primaryImage;
    var swapImageFunc;
    $(".photo-image").hover(function() {
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

    }, function() {
        clearInterval(swapImageFunc);
        $(this).find('.preview-img').attr('src', primaryImage);
    });

});
