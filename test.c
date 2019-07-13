#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<string.h>

#include"ops.h"


unsigned int int_to_int(unsigned int k) {
    return (k == 0 || k == 1 ? k : ((k % 2) + 10 * int_to_int(k / 2)));
}



int main (int argc, char*argv[]) {

    char *msg = "abc";

    // How many bits are used to represent the string
    long size = strlen(msg) * 8;
    printf("%ld\n", size);
    printf("%d\n", int_to_int(size));
    
    int appendix = 0b10000000;

    

    int k = (((512 - 54) % (512)) - (1 + size));

    while (k < 0) {
        k += 512;
    }

    int number_of_blocks = k/512;
    if (k % 512 != 0) {
        number_of_blocks = k/512 + 1;
    }

    printf("Number of blocks: %d\n", number_of_blocks);

    int len = ((number_of_blocks*512) / 8);
    int new_msg[len]; // = malloc(sizeof(msg) + 1);
    int j;
    for (j = 0; j < strlen(msg); j++) {
        new_msg[j] = msg[j];
    }
    new_msg[j] = appendix;

    int k_remain = k%8;
    k = k-k_remain;
    printf("K: %d\n", k);
    printf("K remain: %d\n", k_remain);

    for (int i = 0; i < k/8; i++, j++) {
        new_msg[j] = 0;
    }

    // int appendix_1 = size << k_remain;
    // int appendix_2 = size >> k_remain;
    // new_msg[j] = appendix_1;
    // j++;
    // new_msg[j] = appendix_2;
    // j++;

    for (j; j < len - 1; j++) {
        new_msg[j] = 0;
    }
    new_msg[j] = size;

    // printf("%ld", sizeof(appendix_2));

    printf("\n");
    for (int y = 0; y < len; y++) {
        printf("%d", int_to_int(new_msg[y]));
    }
    printf("\n");

    return 0;
}