$(function () {
    // helper utility to apply a form field error
    function apply_form_field_error(fieldname, error) {
        var container = $("#div_id_" + fieldname);
        container.append(error);
        container.show();
    }

    function clear_errors() {
        $('.ajax-error').hide();
        $('#error_div').hide();
    }

    function reset_login_form() {
        // not ideal - reset height back to original height in case errors happened
        $('#login_modal').get(0).style.height = '485px';
        $('#login_form').get(0).reset();
    }

    // dynamically load in the log in modal when 'login' is clicked on the header
    $(".login").click(function(e) {
        e.preventDefault(); // prevent navigation
        var url = $(this).data("form"); // get the login form url

        $("#login_modal").load(url, function() { // load the url into the modal
            $(this).modal('show'); // display the modal on url load
            reset_login_form();
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
            },
            error: function(data, textStatus, jqXHR) {
                clear_errors();
                // set the height to 550px so no scroll bar appear when there is an error
                $('#login_modal')[0].style.height = '550px';
                var errors = $.parseJSON(data.responseText);
                $.each(errors, function(index, value) {
                    if (index === "__all__") {
                        $('#error_div').html(value);
                        $('#error_div').show();
                    } else {
                        apply_form_field_error(index, value);
                    }
                });
            }

        });
        return false;
    });

    $('#login_modal').on('shown', function() {
        // on click of the 'register' link, hide the login modal, and show the register modal
        $("#register_on_login").click(function(e) {
            e.preventDefault();
            var registerUrl = $(this).data("register"); // used to load the register modal
            $('#login_modal').modal('hide');
            $("#register_modal").load(registerUrl, function() {
                $(this).modal('show');
            });
        });
});

    // REGISTRATION SCRIPTS

    // dynamically load in the log in modal when 'register' is clicked on the header
    $(".register").click(function(e) {
        e.preventDefault(); // prevent navigation
        var url = $(this).data("form"); // get the register form url

        $("#register_modal").load(url, function() { // load the url into the modal
            $(this).modal('show'); // display the modal on url load
        });
        return false; // prevent the click propagation
    });

    $('#register_modal').on('submit', '#registration_form', function() {
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            context: this,
            success: function(data, status) {
                // close the modal and reload the current page
                $('#register_modal').modal('hide');
                window.location.reload(true);
            },
            error: function(data, textStatus, jqXHR) {
                clear_errors();
                // set the height to 600px so no scroll bar appear when there is an error
                $('#register_modal')[0].style.height = '600px';
                var errors = $.parseJSON(data.responseText);
                $.each(errors, function(index, value) {
                    if (index === "__all__") {
                        $('#error_div').html(value);
                        $('#error_div').show();
                    } else {
                        apply_form_field_error(index, value);
                    }
                });
            }

        });
        return false;
    });

    $("#register_modal").on('shown', function() {
        // on click of the 'login' link, hide the register modal, and show the login modal
        $("#login_on_register").click(function(e) {
            e.preventDefault();
            var loginUrl = $(this).data("login"); // get the login url
            $('#register_modal').modal('hide');
            $("#login_modal").load(loginUrl, function() {
                $(this).modal('show');
            });
        });
    });

});