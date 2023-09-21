$(document).ready(() => {
    $("#id_name").attr("onchenge", "searchAlbum(this)")
})

function searchAlbum(input) {
    const albumName = $(input).val();
    const endpoint = $("#endpoint").val();
    const token = $("input[name='csrfmiddlewaretoken']").val()

    const requestData = {
        "album_name": albumName
    };

    $.ajax({
        type: "POST",
        url: endpoint,
        data: requestData,
        headers: {
            "X-CSRFToken": token
        },
        success: (response) => {
            console.log(response)
        },
        error: () => {
            alert("error found")
        }
    });

};