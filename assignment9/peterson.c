#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#define false 0
#define true 1
int favoredProcess = 1;
int P1_WantsToEnter = false;
int P2_WantsToEnter = false; 
int *val;

void* P1(void *args){
	while(true) {
		// printf("p1\n");
		P1_WantsToEnter = true;
		favoredProcess = 2;
		while(P2_WantsToEnter && favoredProcess == 2){					
			printf("\np1 waiting\n");
			// sleep(2); /* busy wait */
		}
		/* Critical section code */
		printf("p1 is running in critical section\n");
		*val = *val + 20;
		sleep(1);
		printf("Updated value after the execution of process1 :%d \n", *val);
		printf("process 1 is out of critical section\n");
		printf("\n");

		// leaving critical section
		
		P1_WantsToEnter = false;
		sleep(2);
		/* Remaining Code */
		// break;
	}

}

void* P2(void *args){
	while(true) {
		// printf("p2\n");
		P2_WantsToEnter = true;
		favoredProcess = 1;
		while(P1_WantsToEnter && favoredProcess == 1){					
			printf("\np2 waiting\n");
			// sleep(2); /* busy wait */
		}
		/* Critical section code */
		printf("p2 is running in critical section\n");
		*val = *val + 10;
		sleep(1);
		printf("Updated value after the execution of process2 :%d \n", *val);
		printf("process 2 is out of critical section\n");
		printf("\n");	
		
		P2_WantsToEnter = false	;
		// break;
		sleep(2);
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
