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
var FileEditor = {
	innerHTML_backup : new Array,
	table_edit_backup : null,
	table_edit_td : null,
	divedit_menu : new Array,
	divedit_file : new Array,

	container_save: function(id) {
      		var element=document.getElementById(id);
       		this.innerHTML_backup[id]=element.innerHTML;
		return element;
	},

	container_restore: function(id) {
        	var element=document.getElementById(id);
     		element.innerHTML=this.innerHTML_backup[id];
		return element;
	},

	textarea_edit: function(id,filename) {
		this.container_save(id);
		xmlhttpget('/cgi-bin/pxe/editfile.cgi?file=' + filename + '&div=' + id,id);
	},

	list: function(subdir) {
		xmlhttpget('/cgi-bin/pxe/editfile.cgi?list=' + subdir,'eval');
	},

	menu_build: function(selectid,container,mode) {
		var i;
		var select;

		select=document.getElementById(selectid);

		i=select.length;
		while (i-- > 0) select.remove(0);

		i=0;
		while (i<this.divedit_menu.length) {
			var opt=document.createElement('option');
			opt.text=this.divedit_menu[i];
			select.add(opt,null);
			++i;
		}
		if (container!=undefined) {
			this.showfile(this.divedit_file[select.selectedIndex],container,mode);
		}
	},

	showfile: function(filename,container,mode) {
		if (this.table_edit_td!=undefined) {
			this.table_edit_td.innerHTML=this.table_edit_backup;
			this.table_edit_td=undefined;
		}
		var id=this.container_save(container);
		xmlhttpget('/cgi-bin/pxe/loadfile.cgi?file=' + filename + '&div=' + container + '&mode=' + mode,container);

	},


	editfile: function(select,editor_filename,container) {
		if (this.table_edit_td!=undefined) {
			this.table_edit_td.innerHTML=this.table_edit_backup;
			this.table_edit_td=undefined;
		}
		var id=this.container_save(container);
		divedit(container,this.divedit_file[select.selectedIndex]);
	},

	table_edit: function(td) {
		var content=td.innerHTML;
		if (this.table_edit_td!=undefined) {
			if (this.table_edit_td==td) {
				return;
			}
			this.table_edit_td.innerHTML=this.table_edit_td.childNodes[0].value;
		}
		this.table_edit_backup=content;
		this.table_edit_td=td;
		td.innerHTML='<input class="editable" type="text" onkeypress="return FileEditor.table_edit_keypress(this,event)" />'
		td.childNodes[0].value=content;
		td.childNodes[0].focus();
	},

	keypress: function(_this,event) {
		var unicode=event.charCode? event.charCode : event.keyCode ;
		if (unicode==13 || unicode==9) {
			_this.table_edit_td.innerHTML=_this.table_edit_td.childNodes[0].value;
			_this.table_edit_td=undefined;
			return false;
		}
		if (unicode==27) {
			_this.table_edit_td.innerHTML=_this.table_edit_backup;
			_this.table_edit_td=undefined;
			return false;
		}

		return true;
	}
}
