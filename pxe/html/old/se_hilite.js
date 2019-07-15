Hilite={
  elementid:'content',
  exact:true,max_nodes:1000,
  onload:true,
  style_name:'hilite',
  style_name_suffix:true,
  debug_referrer:''
};

Hilite.search_engines=[['^http://(www)?\\.?google.*','q='],['^http://search\\.yahoo.*','p='],['^http://search\\.msn.*','q='],['^http://search\\.aol.*','userQuery='],['^http://(www\\.)?altavista.*','q='],['^http://(www\\.)?feedster.*','q='],['^http://search\\.lycos.*','query='],['^http://(www\\.)?alltheweb.*','q=']];

Hilite.decodeReferrer=function(referrer) {
  var query=null;
  var match=new RegExp('');
  for(var i=0;i<Hilite.search_engines.length;i++) {
    match.compile(Hilite.search_engines[i][0],'i');
    if(referrer.match(match)) {
      match.compile('^.*'+Hilite.search_engines[i][1]+'([^&]+)&?.*$');
      query=referrer.replace(match,'$1');
      if(query){
        query=decodeURIComponent(query);
        query=query.replace(/\'|"/,'');
        query=query.split(/[\s,\+\.]+/);
        return query;
      }
    }
  }
  return null;
};

Hilite.hiliteElement=function(elm,query) {
  if (!query||elm.childNodes.length==0) return;
  var qre=new Array();
  for (var i=0;i<query.length;i++) {
    query[i]=query[i].toLowerCase();
    if (Hilite.exact)
      qre.push('\\b'+query[i]+'\\b');
    else
       qre.push(query[i]);
    }
    qre=new RegExp(qre.join("|"),"i");
    var stylemapper={};
    for (var i=0;i<query.length;i++) stylemapper[query[i]]=Hilite.style_name+(i+1);
    
    var textproc=function(node) {
      var match=qre.exec(node.data);
      if(match) {
        var val=match[0];
        var k='';
        var node2=node.splitText(match.index);
        var node3=node2.splitText(val.length);
        var span=node.ownerDocument.createElement('SPAN');
        node.parentNode.replaceChild(span,node2);
        span.className=stylemapper[val.toLowerCase()];
        span.appendChild(node2);
        return span;
      } else {
        return node;
      }
    };
    Hilite.walkElements(elm.childNodes[0],1,textproc);
  };

  Hilite.hilite=function() {
    var q=Hilite.debug_referrer?Hilite.debug_referrer:document.referrer;
    var e=null;
    q=Hilite.decodeReferrer(q);

    if (q && ((Hilite.elementid && (e=document.getElementById(Hilite.elementid))) || (e=document.body))) {
      Hilite.hiliteElement(e,q);
    }
  };

  Hilite.walkElements=function(node,depth,textproc) {
    var skipre=/^(script|style|textarea)/i;
    var count=0;
    while(node&&depth>0) {
      count++;
      if (count>=Hilite.max_nodes) {
        var handler=function() {
          Hilite.walkElements(node,depth,textproc);
        };
        setTimeout(handler,50);
        return;
      }
      if (node.nodeType==1) {
        if (!skipre.test(node.tagName) && node.childNodes.length>0) {
          node=node.childNodes[0];
          depth++;
          continue;
        }
      } else if(node.nodeType==3) {
        node=textproc(node);
      }
      if (node.nextSibling) {
        node=node.nextSibling;
      } else {
        while (depth>0) {
           node=node.parentNode;
           depth--;
           if (node.nextSibling) {
             node=node.nextSibling;
             break;
           }
         }
       }
     }
   };
   
   if (Hilite.onload) {
      if (window.attachEvent) {
        window.attachEvent('onload',Hilite.hilite);
      } else if (window.addEventListener) {
        window.addEventListener('load',Hilite.hilite,false);
      } else {
        var __onload=window.onload;
        window.onload=function() {
           Hilite.hilite();
           __onload();
        };
      }
    }
