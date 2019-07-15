/*
# backuPXE - Copyright (C) 2006-2019 Luc Deschenaux
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
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
