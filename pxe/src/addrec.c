#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE *f=0;

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
	char *usage="usage: addrec <filename> <key> <value>\n";
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

	while(1) {

		c=fgets(buf,bufsize,f);
		if (!c) {
			if (feof(f)) {
				if (argc>3) {
					fprintf(f,"%s",index);
					for(i=3;i<argc;++i) {
						fprintf(f," %s",argv[i]);
					}
					fprintf(f,"\n");
				} else {
					fprintf(f,"%s %s\n",index,value);
				}
				myexit(0);
				
			} else {
				fprintf(stderr,"%s: read error\n",filename);
				myexit(1);
			}
		}
		
		for (i=0;i<len;++i) {
			if ((!buf[i])||(buf[i]!=index[i])) {
				break;
			}
				
		}
		if ((i==len) && ((buf[i]==0) || (buf[i]==' ') || (buf[i]=='\t'))) {
			fprintf(stderr,"%s: exists\n",index);
			myexit(1);
		}
	}
	
	myexit(0);

} // main


void myexit(int code) {
	
	if (f) fclose(f);
	
	exit(code);

} // myexit
