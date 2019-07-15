/**
*
*  Image preload
*  http://www.webtoolkit.info/
*
**/

function ImagePreload() {
	if (typeof(arguments) != 'undefined') {
		for (i=0; i<arguments.length; i++ ) {
			if (typeof(arguments[i]) == "object") {
				for (k=0; k<arguments[i].length; k++) {
					var oImage = new Image;
					oImage.src = arguments[i][k];
				}
			}

			if (typeof(arguments[i]) == "string") {
				var oImage = new Image;
				oImage.src = arguments[i];
			}
		}
	}
}