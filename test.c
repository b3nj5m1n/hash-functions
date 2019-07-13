#include<stdio.h>
#include<stdint.h>

#include"ops.h"


uint32_t Ch32(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (~x & z);
}



int main (int argc, char*argv[]) {

    printf("%d", Ch32(2, 6, 33));

    return 0;
}