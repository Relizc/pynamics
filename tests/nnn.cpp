
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>

#define PI 3.14159265

int main() {
    int i, j;
    double angle = 0.0;
    char cube[5][5] = {
        {'*', '*', '*', '*', '*'},
        {'*', ' ', ' ', ' ', '*'},
        {'*', ' ', ' ', ' ', '*'},
        {'*', ' ', ' ', ' ', '*'},
        {'*', '*', '*', '*', '*'}
    };

    while(1) {
        for(i = 0; i < 5; i++) {
            for(j = 0; j < 5; j++) {
                if(cube[i][j] == '*') {
                    printf("%c", (int)(255 * (0.5 * cos(angle) + 0.5)));
                } else {
                    printf(" ");
                }
            }
            printf("\n");
        }
        angle += PI / 180;
        usleep(100000);
        system("clear");
    }

    return 0;
}