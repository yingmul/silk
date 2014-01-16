// common functions between outfit_detail and piece_detail
$(function () {
    $('#product_carousel').on("click", "img", function() {
        var clickedImg = $(this).attr('src');
        $('.selected-img').attr('src', clickedImg);
    });

    $('#product_carousel').carouFredSel({
        auto: false,
        circular: false,
        height: "variable",
        infinite: false,
        items: {
            width: 100,
            visible: 3
        },
        next: {
            button: "#carousel_next",
            key: "right"
        },
        prev: {
            button: "#carousel_previous",
            key: "left"
        }
    });
});