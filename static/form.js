$(document).ready(() => {
  const preValues = $(".edit-values").text().split(",");
  if (preValues.length > 1) {
    const selectID = $("select").attr("id");
    preValues.forEach(element => {
      let item = createItemText(titleCase(element));
      $(`.${selectID}-selected-list`).append(item);
    });
    addSeletedItems(selectID);
    toggleHelpText(selectID);
  }
})

function updateSelection(y) {
  // y is the selected option
  const text = titleCase($(y).text());
  const item = createItemText(text)  ;
  const parentID = $(y).parent().attr("id");
  const selectTag = $(`#${parentID}`);
  if (!checkItem(text, parentID)) {
    $(`.${parentID}-selected-list`).append(item);
  };
  addSeletedItems(parentID);
}

function createItemText (txt) {
  return `<li class="selected-item" onclick="deleteItem(this)">${txt}</li>`;
}
  
function checkItem(val, parentID) {
  let itemExists = false;
  $(`.${parentID}-selected-list li`).each( function() {
    if ($(this).text() === val) {
      itemExists = true;
      return itemExists;
    }
  });
  return itemExists;
}
  
function deleteItem(x) {
  const parentClass = $(x).parent().attr("class");
  const selectID = parentClass.split("-")[0];
  $(x).remove();
  addSeletedItems(selectID);
  toggleHelpText(selectID);
}
  
function addSeletedItems(parentID) {
  let selectedLabels = [];
  let selectedValues = [];
  const optionTags = $(`#${parentID} option`);

  $(`.${parentID}-selected-list li`).each(function(){
    selectedLabels.push($(this).text());
  });
  optionTags.each(function () {
    if (selectedLabels.includes($(this).text())) {
      selectedValues.push($(this).val());
    }
  });
  $(`#${parentID}`).val(selectedValues) 
}

function titleCase(name) {
  const upperWords = []
  name.split(" ").forEach(element => {
    let upperWord = element.charAt(0).toUpperCase() + element.slice(1);
    upperWords.push(upperWord);
  });
  return upperWords.join(" ")
}

function toggleHelpText(selectID){
  const text = $(".help-item-text");
  if ($(`#${selectID}`).val().length >= 1) {
    text.removeClass("hidden");
  }
  else {
    text.addClass("hidden");
  }
  console.log()
}