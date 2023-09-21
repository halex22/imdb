$(document).ready(() => {
    $(".single-album")
    .on("mouseenter", function() {
      changeGreen(this);
    })
    .on("mouseleave", function() {
      changeBlack(this);
    });

    function changeGreen(element) {
        const img = $(element).children(".cover-container").children("img");
        $(element).children().children("h3").addClass("bigger-text")
        $(img).addClass("image-animated");
        $(element).children().children(".center").addClass("center-h-over");
    }
    
    function changeBlack(element) {
        const img = $(element).children(".cover-container").children("img");
        $(img).removeClass("image-animated");
        $(element).children().children("h3").removeClass("bigger-text")
        $(element).children().children(".center").removeClass("center-h-over");
    }
})


function showToChange() {
    $("#change-vote").toggle("hidden-element");
    $("#rate_form").toggle("hidden-element");
    $("#keep-vote").toggle("hidden-element");
}

function showToAdd() {
    $("#add-vote").toggle("hidden-element");
    $("#rate_form").toggle("hidden-element");
    $("#dont-vote").toggle("hidden-element");
}
