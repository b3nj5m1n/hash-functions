#include<stdio.h>
#include<stdint.h>
#include <math.h>

// Rotate bits of a 32 bit integer to the right by n bits
uint32_t SCHED_ROTR32(uint32_t x, int n)
{
    return (x >> n | x << 32-n) & 0b0000000011111111111111111111111111111111;
}

// Sigma 0 function as specified in FIPS-180-4 4.1.2
uint32_t SCHED_SIGMA0_32(uint32_t x) {
    return SCHED_ROTR32(x, 7) ^ SCHED_ROTR32(x, 18) ^ (x >> 3);
}

// Sigma 1 function as specified in FIPS-180-4 4.1.2
uint32_t SCHED_SIGMA1_32(uint32_t x) {
    return SCHED_ROTR32(x, 17) ^ SCHED_ROTR32(x, 19) ^ (x >> 10);
}

uint32_t MIX(int t, uint32_t init_words[]) {
    if (t >= 16) {
        return (SCHED_SIGMA1_32(init_words[t-2]) + init_words[t-7]+ SCHED_SIGMA0_32(init_words[t-15]) + init_words[t-16]) % (int) pow(2, 32);
    }
    return init_words[t];
}

uint32_t *CREATE_SCHED32(uint32_t init_words[]) {
    uint32_t *W;
    W = malloc(sizeof(uint32_t) * 64);
    for (int t = 0; t < 16; t++) {
        W[t] = MIX(t, init_words);
        printf("%d\n", W[t]);
    }
    for (int t = 16; t < 64; t++) {
        W[t] = MIX(t, W);
        printf("%d\n", W[t]);
    }
    return W;
}