#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<string.h>

#include"ops.h"
#include"prep.h"
#include"sched.h"







int main (int argc, char *argv[]) {

    char *msg = argv[1];

    CREATE_SCHED32(padd(msg));
    

    return 0;
}