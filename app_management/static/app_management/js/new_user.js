$(document).ready(() => {
    $("#id_username")
    .attr("onchange","inputChecker(this, true)")

})

function inputChecker(element, isName) {
    const minLength = isName ? 4 : 8;
    clearMsg(element);
    let msg;
    let _class;
    const currentValue = $(element).val();
    if (isName) {
        if (currentValue.length < minLength) {
            msg = "Username is too short";
            _class = "error-span";
        } else {
            // ajax logic
        }
    } else {
        if (currentValue.length < minLength) {
            msg
        }
    }
    $(element).parent()
    .children(".form-helper")
    .append(`<span class="${_class}">${msg}</span>`);
}

function clearMsg(element) {
    $(element).parent().children("div")
    .children("span").remove();
}