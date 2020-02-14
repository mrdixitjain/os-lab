#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#define false 0
#define true 1
int favoredProcess = 1;
int P1_WantsToEnter = false;
int P2_WantsToEnter = false; 
int *val;

void* P1(void *arg){
	while(true) {
		P1_WantsToEnter = true;
		/* enterMutualExclusion() */
		/* handle deadlock here */
		while(P2_WantsToEnter) {
			if(favoredProcess == 2) {
				P1_WantsToEnter = false;
				while(favoredProcess == 2){
					printf("\np1 waiting\n");
					sleep(2); /* busy wait */
				}
				P1_WantsToEnter = true;
			}
		}
		printf("p1 is running in critical section\n");
		*val = *val + 20;
		printf("Updated value after the execution of process1 :%d \n", *val);
		printf("process 1 is out of critical section\n");
		printf("\n");
		favoredProcess = 2;
		P1_WantsToEnter = false;
		sleep(2);
		// break;
		/* Remaining Code */
	}

}

void* P2(void *args){
	while(true) {
		P2_WantsToEnter = true;
		/* enterMutualExclusion() */
		/* handle deadlock here */
		while(P1_WantsToEnter) {
			if(favoredProcess == 1) {
				P2_WantsToEnter = false;
				while(favoredProcess == 1){					
					printf("\np2 waiting\n");
					sleep(2); /* busy wait */
				}
				P2_WantsToEnter = true;
			}
		}
		printf("p2 is running in critical section\n");
		*val = *val + 10;
		printf("Updated value after the execution of process2 :%d \n", *val);
		printf("process 2 is out of critical section\n");
		printf("\n");	
		favoredProcess = 1;
		P2_WantsToEnter = false;
		sleep(2);
		// break;
	/* Remaining Code */
	}

}
int main(){
	val = (int *)malloc(sizeof(int));
	*val = 0;
	pthread_t pid1, pid2;

	pthread_create(&pid1, NULL, P1, NULL);
	pthread_create(&pid2, NULL, P2, NULL);

	pthread_join(pid1, NULL);
	pthread_join(pid2, NULL);

}
