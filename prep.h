#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<string.h>

unsigned int int_to_int(unsigned int k) {
    return (k == 0 || k == 1 ? k : ((k % 2) + 10 * int_to_int(k / 2)));
}

int *padd(char *msg) {
    // How many bits are used to represent the string
    long size = strlen(msg) * 8;
    // Padd message with 0's
    int k = (((512 - 54) % (512)) - (1 + size));
    while (k < 0) {
        k += 512;
    }
    int number_of_blocks = k/512;
    if (k % 512 != 0) {
        number_of_blocks = k/512 + 1;
    }
    // printf("Number of blocks: %d\n", number_of_blocks);
    // Lenght of array
    int len = ((number_of_blocks*512) / 8);
    // Initalize new array
    int *new_msg;
    new_msg = malloc(sizeof(int) * len);
    // Will be used to keep track of the current index throughout the rest of the function
    int j;
    // Loop over chars in input message
    for (j = 0; j < strlen(msg); j++) {
        new_msg[j] = msg[j];
    }
    // Append 1 to the end
    int appendix = 0b10000000;
    new_msg[j] = appendix;
    // Calculate how many 0's will be left to add
    int k_remain = k%8;
    // Calculate how many 0's can be added as whole bytes
    k = k-k_remain;
    // printf("K: %d\n", k);
    // printf("K remain: %d\n", k_remain);
    // Add those 0's
    for (int i = 0; i < k/8; i++, j++) {
        new_msg[j] = 0;
    }

    // int appendix_1 = size << k_remain;
    // int appendix_2 = size >> k_remain;
    // new_msg[j] = appendix_1;
    // j++;
    // new_msg[j] = appendix_2;
    // j++;

    // Add more 0's until only one byte is left
    for (j; j < len - 1; j++) {
        new_msg[j] = 0;
    }
    // Set last element in array to size of inital message
    new_msg[j] = size;

    // printf("%ld", sizeof(appendix_2));

    // Print array
    printf("\n");
    for (int y = 0; y < len; y++) {
        printf("%d", int_to_int(new_msg[y]));
    }
    printf("\n");

    return new_msg;
}