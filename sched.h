#include<stdio.h>
#include<stdint.h>
#include <math.h>

// Rotate bits of a 32 bit integer to the right by n bits
uint32_t SCHED_ROTR32(uint32_t x, int n)
{
    return x >> n | x << 32-n;
}

// Sigma 0 function as specified in FIPS-180-4 4.1.2
uint32_t SCHED_SIGMA0_32(uint32_t x) {
    return SCHED_ROTR32(x, 7) ^ SCHED_ROTR32(x, 18) ^ (x >> 3);
}

// Sigma 1 function as specified in FIPS-180-4 4.1.2
uint32_t SCHED_SIGMA1_32(uint32_t x) {
    return SCHED_ROTR32(x, 17) ^ SCHED_ROTR32(x, 19) ^ (x >> 10);
}

uint32_t MIX(int t, int init_words[]) {
    if (t >= 16) {
        return (SCHED_SIGMA1_32(init_words[t-2]) + init_words[t-7]+ SCHED_SIGMA0_32(init_words[t-15]) + init_words[t-16]) % (int) pow(2, 32);
    }
    return init_words[t];
}