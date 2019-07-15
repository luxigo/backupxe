/**
*
*  Javascript cookies
*  http://www.webtoolkit.info/
*
**/

function CookieHandler() {

	this.setCookie = function (name, value, seconds) {

		if (typeof(seconds) != 'undefined') {
			var date = new Date();
			date.setTime(date.getTime() + (seconds*1000));
			var expires = "; expires=" + date.toGMTString();
		}
		else {
			var expires = "";
		}

		document.cookie = name+"="+value+expires+"; path=/";
	}

	this.getCookie = function (name) {

		name = name + "=";
		var carray = document.cookie.split(';');

		for(var i=0;i < carray.length;i++) {
			var c = carray[i];
			while (c.charAt(0)==' ') c = c.substring(1,c.length);
			if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
		}

		return null;
	}

	this.deleteCookie = function (name) {
		this.setCookie(name, "", -1);
	}

}
