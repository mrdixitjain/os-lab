#include<bits/stdc++.h>
#include "fun.h"
using namespace std;

int main(){
	int i=0;
	int pid1=fork();
	while(i<5){
		
		ConsumerWait();
		shmid = shmget(cindexkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		cindex=(int *)memory;

		shmid = shmget(conskKey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		lock2=(int *)memory;

		shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		items=(int *)memory;
		ConsumerWait();
		xchg(lock2);
		shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		lock1=(int *)memory;
		xchg(lock1);
		*items=*items-1;
		printf("Consumer just update an item, Total items:%d\n",*items);
		chgLock(lock1,0);
		*cindex+1;
		chgLock(lock2,0);

		sleep(.9);
		
		shmdt(cindex);
		shmdt(items);
		i++;
	}
	exit(0);
}