#include <sys/types.h>
#include <sys/mman.h>
#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#define n 50
#define false 0
#define true 1
/* Array to record which processes are taking a ticket */
int choosing[n]={0};
/* Value of the ticket for each process initialized to 0 */
int ticket[n]={0};
pthread_t pid[n];
int *val;

int maxValue(){
	int max1=0;
	for(int i=0; i<n; i++)
		if(ticket[i]>max1)
			max1=ticket[i];
	return max1;
}



void* Tx(void *args){
	int *a = (int *)args;
	int x = *a;
	choosing[x]=true;
	ticket[x]=maxValue()+1;
	choosing[x]=false;

	for(int i=0;i<n;i++){
		if(i==x)
			continue;
		while(choosing[i]);
			 // sleep(4);
		while(ticket[i]!=0 && ticket[i]<ticket[x]);
			 // sleep(4);
		if(ticket[i]==ticket[x] && i<x){
			while(ticket[i]!=0);
				 // sleep(4);
		}

	}

	printf("\nprocess %d is in critical section\n", x);
	*val=*val+x;
	//val+=2;

	//cout<<"Process "<<x+1<<":val= "<<*val<<endl;
	printf("Updated value after the execution of process %d: %d\n",x, *val);
	printf("process %d is out of critical section\n", x);

	ticket[x]=0;
}

int main(){
	val = (int *)mmap(NULL, sizeof(int), PROT_READ|PROT_WRITE, MAP_ANON|MAP_SHARED, -1, 0);
	*val=0;

	for(int i=0; i<n; i++){
		// printf("creating %d\n", i);
		pthread_create(&pid[i], NULL, Tx, (void *)&i);
	}

	for (int i=0; i<n; i++){
		pthread_join(pid[i], NULL);
	}

}
