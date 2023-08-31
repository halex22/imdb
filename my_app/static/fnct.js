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

$(document).ready(()=> {
    function handleResize() {
        if ($(window).width() <= 750) {
            $(("#album-container").css("display", "block"))
        }
    }
})