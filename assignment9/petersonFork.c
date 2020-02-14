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
		*favoredProcess = 2;
		while(*P2_WantsToEnter && *favoredProcess == 2){					
			printf("\np1 waiting\n");
			sleep(2); /* busy wait */

		}
		/* Critical section code */
		printf("p1 is running in critical section\n");
		*val = *val + 20;
		printf("Updated value after the execution of process1 :%d \n", *val);
		printf("\nprocess 1 is out of critical section\n");
		sleep(2);

		// leaving critical section
		
		*P1_WantsToEnter = false;
		/* Remaining Code */
		break;
	}
}

void P2(){
	while(true) {
		*P2_WantsToEnter = true;
		*favoredProcess = 1;
		while(*P1_WantsToEnter && *favoredProcess == 1){					
			printf("\np2 waiting\n");
			sleep(2); /* busy wait */
		}
		/* Critical section code */
		printf("p2 is running in critical section\n");
		*val = *val + 10;
		printf("Updated value after the execution of process2 :%d \n", *val);
		printf("process 2 is out of critical section\n");
		sleep(2);	
		
		*P2_WantsToEnter = false	;
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
		while(1)
			P2();
		wait();
	}
}

// void* P1(void *args){
// 	while(true) {
// 		// printf("p1\n");
// 		P1_WantsToEnter = true;
// 		favoredProcess = 2;
// 		while(P2_WantsToEnter && favoredProcess == 2){					
// 			printf("\np1 waiting\n");
// 			// sleep(2); /* busy wait */
// 		}
// 		/* Critical section code */
// 		for(int i=0; i<100; i++)
// 			printf(" in P1 ");
// 		// sleep(5);
// 		for(int i=0; i<100; i++)
// 			printf(" in P1 ");

// 		// leaving critical section
		
// 		P1_WantsToEnter = false;
// 		/* Remaining Code */
// 		break;
// 	}

// }

// void* P2(void *args){
// 	while(true) {
// 		// printf("p2\n");
// 		P2_WantsToEnter = true;
// 		favoredProcess = 1;
// 		while(P1_WantsToEnter && favoredProcess == 1){					
// 			printf("\np2 waiting\n");
// 			// sleep(2); /* busy wait */
// 		}
// 		/* Critical section code */
// 		for(int i=0; i<100; i++)
// 			printf(" in P2 ");
// 		// sleep(5);
// 		for(int i=0; i<100; i++)
// 			printf(" in P2 ");
		
// 		P2_WantsToEnter = false	;
// 		break;
// 	/* Remaining Code */
// 	}

// }
// int main(){
// 	pthread_t pid1, pid2;

// 	pthread_create(&pid1, NULL, P1, NULL);
// 	pthread_create(&pid2, NULL, P2, NULL);

// 	pthread_join(pid1, NULL);
// 	pthread_join(pid2, NULL);

// }
