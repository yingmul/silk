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
        // As pointed out in comments,
        // it is superfluous to have to manually call the modal.
        // $('#addBookDialog').modal('show');
    });

});
