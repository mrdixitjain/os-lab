#include <sys/types.h>
#include <sys/mman.h>
#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define false 0
#define true 1

int* favoredProcess;
int* P1_WantsToEnter;
int* P2_WantsToEnter;
int *val;

void P1(){
	while(true) {
		*P1_WantsToEnter = true;
		/* enterMutualExclusion() */
		/* handle deadlock here */
		while(*P2_WantsToEnter) {
			if(*favoredProcess == 2) {
				*P1_WantsToEnter = false;
				while(*favoredProcess == 2){
					printf("\np1 waiting\n");
					sleep(2); /* busy wait */
				}
				*P1_WantsToEnter = true;
			}
			else{
				printf("\np1 waiting\n");
				sleep(2); /* busy wait */
			}
		}
		printf("p1 is running in critical section\n");
		*val = *val + 20;
		printf("Updated value after the execution of process1 :%d \n", *val);
		printf("\nprocess 1 is out of critical section\n");
		sleep(2);
		*favoredProcess = 2;
		*P1_WantsToEnter = false;
		break;
		/* Remaining Code */
	}
}

void P2(){
	while(true) {
		*P2_WantsToEnter = true;
		/* enterMutualExclusion() */
		/* handle deadlock here */
		while(*P1_WantsToEnter) {
			if(*favoredProcess == 1) {
				*P2_WantsToEnter = false;
				while(*favoredProcess == 1){					
					printf("\np2 waiting\n");
					sleep(2); /* busy wait */
				}
				*P2_WantsToEnter = true;
			}
			else{
				printf("\np2 waiting\n");
				sleep(2); /* busy wait */
			}
		}

		printf("p2 is running in critical section\n");
		*val = *val + 10;
		printf("Updated value after the execution of process2 :%d \n", *val);
		printf("\nprocess 2 is out of critical section\n");
		sleep(2);		
		*favoredProcess = 1;
		*P2_WantsToEnter = false;
		break;
	/* Remaining Code */
	}
}

int main(){
	
	favoredProcess = (int *)mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);
	P1_WantsToEnter = (int *)mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);
	P2_WantsToEnter = (int *)mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);
	val = (int *)mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);

	*P1_WantsToEnter=false;
	*P2_WantsToEnter=false;
	*favoredProcess=1;
	*val=0;
	int pid = fork();

	if(pid==0){
		while(1)
			P1();
	}  

	else{
		while(2){
			P2();
		}
			wait();
	}

}
