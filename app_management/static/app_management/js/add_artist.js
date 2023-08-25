$(document).ready(() => {
  $(".input").attr("onmouseenter", "MouseOver(this)")
  $(".input").attr("onmouseout", "MouseOver(this)")
})

function MouseOver(x) {
  $(x).toggleClass("mouse-over-input")
}
