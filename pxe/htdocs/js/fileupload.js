function fileupload(formName,fileName,cgiURL) {
	var request=new XMLHttpRequest();
	if (window.netscape){
		try {
			if (document.location.toString().substr(0,4) != "http") {
				netscape.security.PrivilegeManager.enablePrivilege('UniversalBrowserRead');}
		}
		catch (e) {alert("Unable to enable UniversalBrowserRead privilege !");}
	}		

	var boundary="-----------------------------7918724323452346234"
	var header="";
	header+='--'+boundary+'\r\nContent-Disposition: form-data;';
	header+=' name="'+formName+'"';
	header+=' filename="'+fileName+'"\r\n\r\n';	
	header+=' filename="'+fileName+'"';
	header+='\r\n\r\n'+boundary+'--';	
	var trailer="";
	trailer = '\r\n--' + boundary + '--\r\n';

// to be continued..
}
