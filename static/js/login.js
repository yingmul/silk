$(function () {
    // dynamically load in the log in modal when 'login' is clicked on the header
    $(".login").click(function(e) {
        e.preventDefault(); // prevent navigation
        var url = $(this).data("form"); // get the login form url

        $("#login_modal").load(url, function() { // load the url into the modal
            $(this).modal('show'); // display the modal on url load
        });
        return false; // prevent the click propagation
    });

    $('#login_modal').on('submit', '#login_form', function() {
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data, status) {
                // close the modal and reload the current page
                $('#login_modal').modal('hide');
                window.location.reload(true);
            }
        });
        return false;
    });


});