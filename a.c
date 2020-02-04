#include<stdio.h>
#include<stdlib.h>
#include <sys/ipc.h> 
#include <sys/shm.h> 

int main(){
	int array, cindex, pindex;
	printf("hello");
	cindex=shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT);
	pindex=shmget(IPC_PRIVATE, sizeof(int), IPC_CREAT);
	array=shmget(IPC_PRIVATE, 10*sizeof(int), IPC_CREAT);
	printf("hello");

	int *c = (int *) shmat(cindex, (void*)0, 0);
	int *d = (int *) shmat(pindex, (void*)0, 0);
	printf("hello");
	*c=0;
	*d=0;

	shmdt(c);
	shmdt(d);

	int pid=fork();
		if(pid==0){
			int i=0;
			while(i<10){
				int *a = (int *) shmat(cindex, (void*)0, 0);
				int *b = (int *) shmat(pindex, (void*)0, 0);
				int *arr = (int *) shmat(array, (void*)0, 0);
				while((*a+1)%10==*b){
					printf("producer waiting");
					shmdt(a);
					shmdt(b);
					shmdt(arr);
					sleep(1);

				}
				arr[*a]=rand()%100;
				printf("produced at %d %d\n", *a, arr[*a]);
				*a++;
				*a%=10;
				shmdt(a);
				shmdt(b);
				shmdt(arr);
				sleep(1);
				i++;
			}

		}

		else{
			int i=0;
			while(i<20){
				int *a = (int *) shmat(cindex, (void*)0, 0);
				int *b = (int *) shmat(pindex, (void*)0, 0);
				int *arr = (int *) shmat(array, (void*)0, 0);
				while(*a==*b){
					printf("consumer waiting");
					shmdt(a);
					shmdt(b);
					shmdt(arr);
					sleep(1);

				}
				printf("consumed at %d %d\n", *b, arr[*b]);
				*b++;
				*b%=10;
				shmdt(a);
				shmdt(b);
				shmdt(arr);
				sleep(1);
				i++;
			}

		}
	}