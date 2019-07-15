#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <time.h>

char *usage="usage: modtime <path>\n";

int main(int argc, char **argv) {
	struct stat st;
	struct tm *t;

	if (argc!=2) {
		fprintf(stderr,"%s",usage);
		exit(1);
	}

	if (stat(argv[1],&st)<0) {
		return errno;
	}

	t=localtime(&st.st_mtime);

	fprintf(stdout,"%d-%02d-%02d %02d%02d.%02d\n",1900+t->tm_year,t->tm_mon+1,t->tm_mday,t->tm_hour,t->tm_min,t->tm_sec);
//	fprintf(stdout,"%lu",(unsigned long)st.st_mtime);
	exit(0);
}
