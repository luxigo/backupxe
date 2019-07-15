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
					fprintf(stderr,"%s: no match (%s) \n",index,filename);
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

			if (!buf[i])
				exit(0);
			++i;
			
			if (1) {
				fprintf(stdout,"%s",buf+i);
				exit(0);

			} else {
				if (lastmatch)
					free(lastmatch);
				
				lastmatch=strdup(buf+i);
			}
		}
		
	}
	exit(1);
} // main

