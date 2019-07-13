#include<stdio.h>
#include<stdint.h>

// Rotate bits of a 32 bit integer to the right by n bits
uint32_t ROTR32(uint32_t x, int n)
{
    return x >> n | x << 32-n;
}

// Rotate bits of a 64 bit integer to the right by n bits
uint64_t ROTR64(uint64_t x, int n)
{
    return x >> n | x << 64-n;
}

// Sigma function as specified in FIPS-180-4 4.1.2
uint32_t SIGMA0_32(uint32_t x) {
    return ROTR32(x, 2) ^ ROTR32(x, 13) ^ ROTR32(x, 22);
}