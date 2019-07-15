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

