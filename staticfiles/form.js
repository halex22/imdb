$(document).ready(() => {
  const preValues = $("#pre-values").val().split(",");
  if (preValues.length > 1) {
    const selectID = $("select").attr("id");
    const labels = changeNumberToLabel(selectID, preValues)
    labels.forEach(element => {
      let item = createItemText(titleCase(element));
      $(`.${selectID}-selected-list`).append(item);
    });
    addSeletedItems(selectID);
    toggleHelpText(selectID);
  }
})

function changeNumberToLabel(parentID, preValues) {
  const optionTags = $(`#${parentID} option`);
  let foundLabels = []
  optionTags.each(function() {
    if (preValues.includes($(this).attr("value"))) {
      foundLabels.push($(this).text())
    }
  })
  return foundLabels
}

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
  toggleHelpText(parentID);
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
  const text = $(`.${selectID}-help-item-text`);
  if ($(`#${selectID}`).val().length > 0) {
    text.removeClass("hidden");
  }
  else {
    text.addClass("hidden");
  }
}