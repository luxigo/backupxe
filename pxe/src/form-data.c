#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

char *USAGE="usage: form-data <headers_output_filename> <boundary> <nextline_substring> [<nextline_substring> ...] <input_file>\n";

char *memstr(char *buf,size_t len,char *str) {

	size_t p=0;
	size_t i=0;
	size_t slen=strlen(str);
	char *start=0;

	while (p<len) {
		if (buf[p]==str[i]) {
			if (!start) start=buf+p;
			++i;
			if (i==slen) {
#ifdef DEBUG
				fprintf(stderr,"\nmatch! %s\n",str);
#endif
				return start;
			}
#ifdef DEBUG
			if (i==40) 
				fprintf(stderr,"\ni=40\n"); 
#endif

		} else {
			if (i) {
					i=0;
					start=0;
					continue;
			}
		}
		++p;
	}

	if (i>0) {
		return (char*)-1;
	}
	return 0;
}

int main(int argc,char **argv) {

	char *c;
	char *buf;
	int level=2;
	int lasterrlevel=0;
	size_t offset;
	char *boundary;
	FILE *f;
	FILE *outf;
	int header;
	char *header_filename;
	unsigned long start;

	if (argc<4) {
		fprintf(stderr,"%s",USAGE);
		exit(1);
	}

//if i call fopen after strcpy, the content of var boundary is garbled !!??
//using gcc version 4.1.1 (Gentoo 4.1.1) and gcc version 4.1.2 20060928 (prerelease) (Ubuntu 4.1.1-13ubuntu5)

	if (!strcmp(argv[argc-1],"-")) {
		f=stdin;
	} else if (!(f=fopen(argv[argc-1],"r"))) {
		fprintf(stderr,"form-data: cant open file (%d)",errno);
		exit(1);
	}

	header_filename=argv[1];
	if ((header=open(header_filename,O_WRONLY|O_TRUNC|O_CREAT))==-1) {
		fprintf(stderr,"form-data: cant open %s for writing (%d)",header_filename,errno);
		exit(1);
	}

// gdb output confirms the bug:
//102             if (!(header=fopen(header_filename,"w"))) {
//(gdb) print boundary
//$1 = 0x804b170 "\r\n", '-' <repeats 29 times>, "AaB03x"
//(gdb) step
//108                     fprintf(header,"%s",buf);
//(gdb) print boundary
//$2 = 0x804b170 "\r\n", '-' <repeats 18 times>, "i\001"
//
	buf=malloc(8192);
	if (!buf) {
		fprintf(stderr,"form-data: out of memory !");
		exit(1);
	}
//-------------------
	boundary=malloc(strlen(argv[2]+16));
	if (!boundary) {
		exit(1);
	}
	boundary[0]='\r';
	boundary[1]='\n';
	boundary[2]='-';
	boundary[3]='-';
	strcpy(boundary+4,argv[2]);
//---------------------------------------
//
	while(level<(argc-1)) {

		c=fgets(buf,4096,f);
		if ((!c) || (feof(f))) {
			fprintf(stderr,"form-data: eof1\n");
			exit(1);
		}

		c=strstr(buf,argv[level]);
		if (c) {
			fprintf(stderr,"form-data: got %s at %x\n",argv[level],(unsigned long)(c-buf)+ftell(f)-strlen(buf)+3);
			++level;
			lasterrlevel=0;

		} else {
			if (level!=lasterrlevel) {
				fprintf(stderr,"form-data: no match for %s\n",argv[level]);
				lasterrlevel=level;
			}
			level=2;
		}
	}

	do {
		write(header,buf,strlen(buf));
		c=fgets(buf,4096,f);
                if ((!c) || (feof(f))) {
			fprintf(stderr,"form-data: eof2\n");
                        exit(1);
                }
	} while((buf[0]!='\x0d') || (buf[1]!='\x0a') || (buf[2]));
	close(header);

	outf=stdout;
	c=0;
	offset=0;
	start=ftell(f);
	fprintf(stderr,"form-data: data start at %x\n",start);
	while(!feof(f) && !c) {
		int d;
		size_t r;
		size_t w;
		if (offset) {
#ifdef DEBUG
		fprintf(stderr,"moving %lu bytes\n",offset);
#endif
			memmove(buf,buf+r,offset);
		}
		if(!(r=fread(buf+offset,1,4096-offset,f))) {
			if (!feof(f)) {
				fprintf(stderr,"form-data: read error\n");
			}
			break;
		}
#ifdef DEBUG
		fprintf(stderr,"read %lu bytes\n",r);
#endif
		r+=offset;
		offset=0;
		if (c=memstr(buf,r,boundary)) {
#ifdef DEBUG
		fprintf(stderr,"c=%ld\n",c);
#endif
			if (c==(char*)-1) {
				c=0;
				if (buf+r-strlen(boundary)>buf) {
					offset=strlen(boundary);
					r-=offset;
				} else {
					fprintf(stderr,"You are doomed!\n");
						exit(1);
				}
			} else {
				unsigned long pos=(unsigned long)(c-buf)+ftell(f)-r;
				fprintf(stderr,"form-data: got trailer at %x, data length=%lu\n",pos,pos-start+1);
				r=(size_t)(c-buf);
			}
		}
#ifdef DEBUG
		fprintf(stderr,"writing %lu bytes\n",r);
#endif
		if ((w=fwrite(buf,1,r,outf))!=r) {
			fprintf(stderr,"form-data: write error\n");
			exit(1);	
		}
	}

	fflush(outf);

	if ((!c) || (c==(char*)-1)) {
		fprintf(stderr,"nomatch\n");
		return 1;
	}	
	return 0;
}
