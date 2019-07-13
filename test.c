#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<string.h>

#include"ops.h"
#include"prep.h"
#include"sched.h"







int main (int argc, char *argv[]) {

    char *msg = argv[1];

    padd(msg);

    printf("%d", SCHED_SIGMA1_32(5));
    

    return 0;
}