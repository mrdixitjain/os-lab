// implementation of Eisenberg and Mcguires algorithm
// done by Dixit Kumar Jain
// date : march 29, 2020


// in critical section, each process adds it's process number to a shared variable.


#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define n 6 // total number of process will be 2^n-1
#define N (int)pow(2, n) // N = total number of processes - 1

int *flags; // flag[i] = 0 => idle, flag[i] = 1 => waiting, flag[i] = 2 => active
int *turn;  // stores the number of process whose turn is next.
int *noOfProcess; // number of process
int *value; // shared variable

void startProcess(int num) {
	// printf("%d\n", num);
	int index;

	do {
		// printf(".");
		// process num tell everybody that he wants in.
		flags[num] = 1; 

		/* num wait until a sweep from "turn" around "clockwise" to num finds everyone 
        idle -- they have "priority" over num right now.*/
		index = *turn;
		// printf("%d %d\n", num, *turn);
		while(index != num) {
			// printf("%d ", num);
			if(flags[index] != 0){
				index = *turn;
				// sleep(1);
			}
			else
				index = (index + 1)%N;
		}

		// num tells everybody that it's in the critical section. (but it's NOT!)

		flags[num] = 2;

		// search the whole ring for someone besides num with flag = "active"
		index = 0;
		while((index < N) && ((index == num) || (flags[index] != 2))) {
			index = (index + 1);
		}
		/* if (the search fails) and ( (it's num's turn) or (P*, the process whose turn it 
     is, is idle)) then num goes in to the CS.  If not, num starts over at 1. */
	} while(!((index >= N) && ((*turn == num) || (flags[*turn] == 0))));

	*turn = num;  // (* It is num's turn, and num goes in.
	// critical section

	*value += num;

	printf("%d -> %d\n", num, *value);

	/* (* num finds the first process clockwise from "turn" who is not idle, and make it 
     be the turn of THAT process. (Note: "turn" is num's when num starts this, and it 
    will still be num's turn after lines 7, if everyone else is idle.) */

	index = (*turn+1)%N;

	while (flags[index] == 0) {

		index = (index+1)%N;

	}
	/* give the turn to someone that needs it, or keep it */
	*turn = index;

	/* we're finished now */
	flags[num] = 0; // num tells everybody that it's idle.
}

int main() {
	srand(time(0));
	flags = (int *)mmap(NULL, sizeof(int)*N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	turn = (int *)mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	noOfProcess = (int *)mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	value = (int *)mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	*value = 0;
	*turn = rand()%(N-1);
	*noOfProcess = rand()%(N-1);
	// printf("%d\n", *turn);
	for(int i = 0; i < N-1; i++) {
		flags[i] = 0;
	}


	int i = 0; 
	// printf("%d\n", N);
	for(int i = 0; i < n; i++){
		// printf("i = %d\n", i);
		int pid = fork();

		if(pid < 0){
			printf("Processes are not created\n");
		}
		else if(pid > 0){
			int num = *noOfProcess;
			*noOfProcess = (*noOfProcess + 1)%(N-1);
			startProcess(num);
		}
	}

}