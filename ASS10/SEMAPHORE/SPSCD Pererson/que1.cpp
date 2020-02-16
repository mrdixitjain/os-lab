#include<bits/stdc++.h>
#include "fun.h"
using namespace std;


int main(){
	
	shmid = shmget(cindexkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	cindex=(int *)memory;
	*cindex=0;

	shmid = shmget(pindexkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	pindex=(int *)memory;
	*pindex=0;


	shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);

	memory = shmat(shmid,NULL,0);

	p=(int*)memory;
	for(int i=0;i<n;i++){
		p[i]=i;
	}

	retval = shmdt(p);
	shmdt(cindex);
	shmdt(pindex);
	//cout<<"Hello YASHSB";

	//for check initialy semaphor works or not

	if(fork()==0){//Consumer code
		int i=0;
		while(i<5){
			shmid = shmget(cindexkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			cindex=(int *)memory;
			shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			p=(int*)memory;
			p[*pindex%n]=rand()%100;

			while(*cindex%n!=*pindex);
			sleep(1);
			printf("Producer just update an item, Total items:%d\n",*items);
			*pindex=*pindex+1;
			
			*cindex+=1;

			sleep(.9);
			printf("Consumer just update an item, Total items:%d\n",*items);
			shmdt(cindex);
			shmdt(p);
			i++;
		}
		exit(0);
	}
	else{//Producer Code
		int i=0;
		//int pid =fork();
		//int pid1=fork();
		while(i<15){
			shmid = shmget(pindexkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			pindex=(int *)memory;

			shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			p=(int*)memory;
			p[*pindex%n]=rand()%100;

			while(*cindex%n==*pindex%n+1);
			sleep(1);
			printf("Producer just update an item, Total items:%d\n",*items);
			*pindex=*pindex+1;
			shmdt(p);
			shmdt(pindex);
			i++;
		}
		exit(0);
	}
	exit(0);
}
