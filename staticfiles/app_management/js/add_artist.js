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

function updateSelection(x) {
  const item = `<li class="selected-item" onclick="deleteItem(this)">${x}</li>`
  if (!checkItem(x)) {
    $(".selected-list").append(item);
  };
  addSeletedItems();
  console.log($("#id_subgenres").val());
}

function checkItem(val) {
  let itemExists = false;
  $(".selected-list li").each( function() {
    if ($(this).text() === val) {
      itemExists = true;
      return itemExists;
    }
  });
  return itemExists;
}

function deleteItem(x) {
  $(x).remove();
}

function addSeletedItems() {
  let items = [];
  $(".selected-list li").each(function(){
    items.push($(this).text());
  });
  $("#id_subgenres").val(items);
}