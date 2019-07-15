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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc,char **argv);

int main(int argc,char **argv) {

	char *filename;
	FILE *f;
	char *buf;
	char *c;
	char *index;
	size_t len;
	size_t i;
	size_t bufsize;
	char *lastmatch=0;

	filename=argv[1];
	index=argv[2];

	if (!index[0]) {
		fprintf(stderr,"null index\n");
		exit(1);
	}

	len=strlen(index);
	bufsize=len+2048;
	buf=(char*)calloc(1,bufsize);
	if (!buf) {
		fprintf(stderr,"%s: out of memory..\n",argv[0]);
		exit(1);
	}

	f=fopen(filename,"r");
	if (!f) {
		fprintf(stderr,"%s: cannot open file\n",filename);
		exit(1);
	}

	while(1) {
		c=fgets(buf,bufsize,f);
		if (!c) {
			if (feof(f)) {
				if (lastmatch) {
					fprintf(stdout,"%s",lastmatch);
					exit(0);
				} else {
					fprintf(stderr,"%s: no match\n",index);
					exit(1);
				}
			} else {
				fprintf(stderr,"%s: read error\n",filename);
				exit(1);
			}
		}

		for (i=0;i<len;++i) {
			if ((!buf[i])||(buf[i]!=index[i])) {
				break;
			}
		}

		if ((i==len) && ((buf[i]==0) || (buf[i]==' ') || (buf[i]=='\t'))) {

			++i;

			if (0) {
				fprintf(stdout,"%s",buf+i);
				exit(0);

			} else {
				if (lastmatch)
					free(lastmatch);

				lastmatch=(buf[i])?strdup(buf+i):strdup("");
			}
		}

	}

} // main
