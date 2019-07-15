/**
*
*  Unselectable text
*  http://www.webtoolkit.info/
*
**/

var Unselectable = {

	enable : function(e) {
		var e = e ? e : window.event;

		if (e.button != 1) {
			if (e.target) {
				var target = e.target;
			} else if (e.srcElement) {
				var target = e.srcElement;
			}

			if (target && target.tagName) {
				var targetTag = target.tagName.toLowerCase();
				if ((targetTag != "input") && (targetTag != "textarea")) {
					return false;
				}
			}
		}
	},

	disable : function () {
		return true;
	}

}

if (typeof(document.onselectstart) != "undefined") {
	document.onselectstart = Unselectable.enable;
} else {
	document.onmousedown = Unselectable.enable;
	document.onmouseup = Unselectable.disable;
}