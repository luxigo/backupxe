/**
*
*  Compute not inline styles
*  http://www.webtoolkit.info/
*
**/

function getStyle(el, property) {
	if (!el) { return null; }

	if (el.currentStyle) {
		var tmp = property.split('-');
		property = tmp[0];

		for (var i = 1; i < tmp.length; i++) {
			property += tmp[i].slice(0, 1).toUpperCase() + tmp[i].slice(1);
		}

		return el.currentStyle[property];
	} else if (window.getComputedStyle) {
		return document.defaultView.getComputedStyle(el, null).getPropertyValue(property);
	}

	return null;
}