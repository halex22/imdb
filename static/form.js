function updateSelection(x, y) {
    const item = `<li class="selected-item" onclick="deleteItem(this)">${x}</li>`;
    const parentID = $(y).parent().attr("id");
    console.log(parentID)
    if (!checkItem(x)) {
      $(`.${parentID}-selected-list`).append(item);
    //   $(".selected-list").append(item);
    };
    addSeletedItems();
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
  }