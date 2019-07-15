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
function xmlhttpget(request,target,waitmessage,param) {
        xmlhttpreq(request,null,target,waitmessage,param);
}

function xmlhttpgetsync(request,target) {
        var xhr;
        if(window.XMLHttpRequest)
                xhr = new XMLHttpRequest();
        else if(window.ActiveXObject)
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
        else {
                alert("Votre navigateur ne supporte pas les objets XMLHTTPRequest...");
                return;
        }
        xhr.open('GET',request,false);
	xhr.send(null);
	if (target!=undefined) {
		document.getElementById(target).innerHTML=xhr.responseText;
	}
}

function xmlhttppost(request,data,target,waitmessage,param) {
        xmlhttpreq(request,data,target,waitmessage,param);
}


function xmlhttpreq (request,data,target,waitmessage,param) {

        var xhr;
	var container;
	var waitmessage;
	var script;

        if(window.XMLHttpRequest)
                xhr = new XMLHttpRequest();
        else if(window.ActiveXObject)
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
        else {
                alert("Votre navigateur ne supporte pas les objets XMLHTTPRequest...");
                return;
        }
        xhr.open(data!=null?'POST':'GET',request,true);
	if (param==undefined)
		param='';

        if (target!=undefined) {

                if (target!='eval') {
			if (target.innerHTML!=undefined) {
				container=target;
			} else {
				container=document.getElementById(target);
				if (container==undefined) {
					container=target;
				}

			}
			if (waitmessage!=undefined) {
				container.innerHTML=waitmessage;
			}

			xhr.onreadystatechange = function() { if (xhr.readyState == 4) { if (container.innerHTML==undefined) { eval(container+"=\""+xhr.responseText+"\""); } else { container.innerHTML=xhr.responseText; } ; eval(param); }  };

		} else {

			eval('xhr.onreadystatechange = function() { if (xhr.readyState == 4) { if (xhr.status==200) { eval(xhr.responseText); ' + param + ' } } }');
		}
        } else {
			eval('xhr.onreadystatechange = function() { if (xhr.readyState == 4) { if (xhr.status==200) { ' + param + ' } } }');
        }
        xhr.send(data);
}
