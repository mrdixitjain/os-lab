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

	shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	items=(int *)memory;
	*items=0;

	shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);

	memory = shmat(shmid,NULL,0);

	p=(int*)memory;
	for(int i=0;i<n;i++){
		p[i]=i;
	}

	shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	lock1=(int *)memory;
	*lock1=0;
	retval = shmdt(p);
	shmdt(cindex);
	shmdt(pindex);
	shmdt(items);
	shmdt(lock1);
	


	if(fork()==0){
		int i=0;
		while(i<5){
			ConsumerWait();
			shmid = shmget(cindexkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			cindex=(int *)memory;

			shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			items=(int *)memory;
			
			shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			lock1=(int *)memory;
			xchg(lock1);
			
			*items=*items-1;
			*cindex+1;
			sleep(.9);
			printf("Consumer just update an item, Total items:%d\n",*items);
			shmdt(cindex);
			shmdt(items);
			chgLock(lock1,0);
			shmdt(lock1);
			i++;
		}
	}
	else{
		//Producer Code
		int i=0;
		//int pid =fork();
		//int pid1=fork();
		while(i<15){
			ProducerWait();
			shmid = shmget(pindexkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			pindex=(int *)memory;

			shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			p=(int*)memory;
			p[*pindex%n]=rand()%100;

			shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			lock1=(int *)memory;
			xchg(lock1);
			*pindex+=1;
			shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
			memory = shmat(shmid,NULL,0);
			items=(int *)memory;
			*items=*items+1;
			sleep(1);
			printf("Producer just update an item, Total items:%d\n",*items);
			chgLock(lock1,0);
			shmdt(items);
			shmdt(p);
			shmdt(lock1);
			i++;
		}
	}
exit(0);
}
