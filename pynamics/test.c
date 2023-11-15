
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <Python.h>

int fputs(const char *, FILE *) {
	
}

int main() {
	FILE *fp = fopen("write.txt", "w");
	fputs("Real Python!", fp);
	fclose(fp);
	return 1;
}
