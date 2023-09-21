function addSelectedFilter(txt) {
    const selectedFilters = $(".selected-filters ol");
    const n = $(selectedFilters).children().length;
    const li = `<li class="filter-item" id="filter-${txt}"><b>${n+1}. ${txt}</b></li>`;
    selectedFilters.append(li);
    document.getElementById(`filter-${txt}`).style.color = `var(--item${n})`
}

function removeSelectFilter(text) {
    const toRemove = $(`#filter-${text}`);
    toRemove.remove();
}

function filterOptn(element) {
    const inputName = $(element).attr("name");
    const txt = $(`label[for='${inputName}']`).text();
    console.log("text is:"+txt);
    if (!foundListItem(txt)) {
        addSelectedFilter(txt);
    } else {
        document.getElementById(`filter-${txt}`).remove();
        updateColors();
    }
}

function foundListItem(text) {
    let found = false;
    const ulElement = $(".selected-filters ol li");
    let currentListItems = [];

    ulElement.each(function () {
        currentListItems.push($(this).text().split(". ")[1]);
    });
    if (currentListItems.includes(text)) {
        found = true;
        return found
    }
    return found
}

function updateColors() {
    const selectedFilters = $(".selected-filters ol");
    const items = selectedFilters.children();

    items.each(function (index) {
        const textElement = $(this);
        const text = textElement.text().split(". ")[1];
        const newText = `${index + 1}. ${text}`;
        textElement.css("color", `var(--item${index})`);
        textElement.css("font-weight", "bolder");
        textElement.text(newText);
    });
}