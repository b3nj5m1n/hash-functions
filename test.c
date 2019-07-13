#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<string.h>

#include"ops.h"
#include"prep.h"







int main (int argc, char *argv[]) {

    char *msg = argv[1];

    padd(msg);
    

    return 0;
}