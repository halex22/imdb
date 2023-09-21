$(document).ready(() => {
    $("#id_username")
    .attr("onchange","inputChecker(this, true)");
    $("#id_password1")
    .attr("onchange", "inputChecker(this, false)");
    $("#id_password2")
    .attr("onchange", "comparePassword(this, false)");
})

function inputChecker(element, isName) {
    const minLength = isName ? 4 : 8;
    clearMsg(element);
    let msg, _class;
    const currentValue = $(element).val();

    if (currentValue.length < minLength) {
        $(element).addClass("is-invalid");
        const addition = `, please add ${minLength - currentValue.length} characters</span>`;
        _class = "error-span";
        msg = isName ? "Username is too short"+addition: "Password is to short"+addition;
    } else {
        $(element).removeClass("is-invalid");
        msg = isName ? "Username's length is ok": "Password length is OK";
        _class = "ok-span"
    }
    changeMsg(element, _class, msg)
}

function clearMsg(element) {
    $(".errorlist").remove();
    $(element).parent().children("div")
    .children("span").remove();
}

function comparePassword(element) {
    clearMsg(element);
    const pass_1 = $("#id_password1").val();
    const pass_2 = $(element).val();
    let msg, _class;
    if (pass_1 === pass_2) {
        msg = "Both password are the same";
        _class = "ok-span";
    } else {
        msg = "There's something different in the password";
        _class = "error-span"
    }
    changeMsg(element, _class, msg);
}

function changeMsg(element, _class, msg) {
    $(element).parent()
    .children(".form-helper")
    .append(`<span class="${_class}">${msg}</span>`);
}