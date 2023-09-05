$(document).ready(() => {
  $("input#id_name").attr("onchange", "searchArtist(this)");
})

function searchArtist(input) {
  const artistName = $(input).val();
  const endpoint = $("#endpoint").val();
  const token = $("input[name='csrfmiddlewaretoken']").val()

  const requestData = {
    "artist_name": artistName
  }

  $.ajax({
    type: "POST",
    url:endpoint,
    data: requestData,
    headers: {'X-CSRFToken': token},
    success: (res) => {
      console.log(res);
      if (res["message"] !== null) {
        showFoundArtist(res["message"]);
      } else {
        $(".found-artist-section").css("display", "none");
      }
    },
    error: (res) => {
      alert("error")
    }
  })
};

function showFoundArtist(id) {
  $(".found-artist-section").css("display","block");
  $("#found_pk").attr("href", `/artist/${id}`)
}