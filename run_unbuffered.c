#include <stdio.h>
#include <stdlib.h>

int main() {
    setvbuf(stdout, NULL, _IONBF, 0); // Disable stdout buffering
    return system("tempcode.exe");    // Run your compiled C program
}
