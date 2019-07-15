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
#include <sys/types.h>
#include <unistd.h>

char TMPFILE[256];
FILE *f=0;
FILE *outf=0;

int main(int argc,char **argv);
void myexit(int code);

int main(int argc,char **argv) {

	char *filename;
	char *buf;
	char *c;
	char *index;
	char *value;
	size_t len;
	size_t i;
	size_t bufsize;
	char found;
	char *usage="usage: setrec <filename> <key> <value>\n";
	size_t r;
	size_t w;

	if (argc<3) {
		fprintf(stderr,"%s",usage);
		exit(1);
	}

	filename=argv[1];
	index=argv[2];
	value=argv[3];

	if (!index[0]) {
		fprintf(stderr,"null index\n");
		exit(1);
	}

	len=strlen(index);
	bufsize=len+2048;
	buf=(char*)calloc(1,bufsize+1);
	if (!buf) {
		fprintf(stderr,"%s: out of memory..\n",argv[0]);
		exit(1);
	}

	f=fopen(filename,"r+");
	if (!f) {
		fprintf(stderr,"%s: cannot open file\n",filename);
		exit(1);
	}

	sprintf(TMPFILE,"/dev/shm/setrec.%d.tmp",getpid());
	outf=fopen(TMPFILE,"w+");
	if (!outf) {
		fprintf(stderr,"%s: cannot open file for writing\n",TMPFILE);
		myexit(1);
	}

	while(!feof(f)) {

		c=fgets(buf,bufsize,f);
		if (!c) {
			if (feof(f)) {
				if (argc>3) {
					fprintf(outf,"%s",index);
					for(i=3;i<argc;++i) {
						fprintf(outf," %s",argv[i]);
					}
					fprintf(outf,"\n");
				} else {
					fprintf(outf,"%s %s\n",index,value);
				}
				break;
			} else {
				fprintf(stderr,"%s: read error\n",filename);
				myexit(1);
			}

		}

		for (i=0;i<len;++i) {

			if ((!buf[i]) || (buf[i]!=index[i])) {
				fprintf(outf,"%s",buf);
				break;
			}
		}

		if ((i==len) && ((buf[i]==0) || (buf[i]==' ') || (buf[i]=='\t'))) {

			if (argc>3) {
				fprintf(outf,"%s",index);
				for(i=3;i<argc;++i) {
					fprintf(outf," %s",argv[i]);
				}
				fprintf(outf,"\n");
			} else {
				fprintf(outf,"%s %s\n",index,value);
			}

			while(!feof(f)) {

				r=fread(buf,1,bufsize,f);
				if (!r) {
					if (ferror(f)) {
						fprintf(stderr,"%s: read error\n",filename);
						myexit(1);
					}
					break;
				}

				w=fwrite(buf,1,r,outf);
				if (!w) {
					fprintf(stderr,"%s: write error\n",TMPFILE);
					myexit(1);
				}
			}
			break;
		}
	}

	fseek(f,0,SEEK_SET);
	fseek(outf,0,SEEK_SET);

	while(!feof(outf)) {

		r=fread(buf,1,bufsize,outf);
		if (!r) {
			if (ferror(outf)) {
				fprintf(stderr,"%s: read error\n",TMPFILE);
				myexit(1);
			}
			break;
		}

		w=fwrite(buf,1,r,f);
		if (!w) {
			fprintf(stderr,"%s: write error\n",filename);
			myexit(1);
		}

	}

	if (ftruncate(fileno(f),ftell(outf))) {
		fprintf(stderr,"%s: cannot truncate file\n");
		myexit(1);
	}

	myexit(0);
}

void myexit(int code) {

	if (outf) fclose(outf);
	if (f) fclose(f);
	if (outf) remove(TMPFILE);

	exit(code);
}
