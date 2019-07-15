// Global object to hold drag information.

var mousex;
var mousey;

function getmousepos(event) {
  if (browser.isIE) {
    mousex = window.event.clientX + document.documentElement.scrollLeft
      + document.body.scrollLeft;
    mousey = window.event.clientY + document.documentElement.scrollTop
      + document.body.scrollTop;
  }
  if (browser.isNS) {
    mousex = event.clientX + window.scrollX;
    mousey = event.clientY + window.scrollY;
  }
}
