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
