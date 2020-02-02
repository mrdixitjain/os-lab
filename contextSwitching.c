#include <stdio.h> 
#include <stdlib.h> 
#include<time.h> 
#include<pthread.h>
int pindex=0;
int cindex=0, i=0, j=0;

int n=10;
int array[10];

void* producer(){
		while(i<20){
			while((pindex+1)%n==cindex){
				printf("producer waiting\n", cindex, pindex);
				sleep(rand()%3);
			}
			array[pindex]=rand()%100;
			printf("written at %d %d\n", pindex, array[pindex]);
			pindex+=1;
			pindex%=n;
			sleep(rand()%3);
			i++;
		}
}

void* consumer(){
		while(j<20){
			while(cindex==pindex){
				printf("consumer waiting\n");
				sleep(rand()%3);
			}
			printf("read from %d %d\n", cindex, array[cindex]);
			cindex++;
			cindex%=n;
			j++;
			sleep(rand()%3);
		}
}

int main(){

	srand(time(0)); 

	pthread_t pt1, pt2;
	pthread_create(&pt1, NULL, producer, NULL);
	pthread_create(&pt2, NULL, consumer, NULL);
	pthread_join(pt1, NULL);
	pthread_join(pt2, NULL);
}