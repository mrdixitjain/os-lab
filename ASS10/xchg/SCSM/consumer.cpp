#include<bits/stdc++.h>
#include "fun.h"
using namespace std;

int main(){
	
int i=0;
while(i<5){
	ConsumerWait();
	shmid = shmget(cindexkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	cindex=(int *)memory;


	shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	lock1=(int *)memory;
	xchg(lock1);
	shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	items=(int *)memory;
	*items=*items-1;
	*cindex+1;
	sleep(.9);
	printf("Consumer just update an item, Total items:%d\n",*items);
	shmdt(cindex);
	shmdt(items);
	chgLock(lock1,0);
	i++;
}
exit(0);
}