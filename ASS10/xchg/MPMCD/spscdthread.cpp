#include<bits/stdc++.h>
#include "fun.h"
using namespace std;

void ConsumerWait1(){
	while(1){
		shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		items=(int *)memory;
		if(*items>0){
			break;
		}
		shmdt(items);
	}
}

void ProducerWait1(){
	while(1){
		shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		items=(int *)memory;
		if(*items<n-1){
			break;
		}
		shmdt(items);
	}
}

void ProducerFun(){
//Producer Code
int i=0;
	int pid =fork();
	int pid1=fork();
	while(i<15){
		
		ProducerWait();
		shmid = shmget(pindexkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		pindex=(int *)memory;

		shmid = shmget(buffkey,sizeof(int)*n,IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		p=(int*)memory;

		shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		items=(int *)memory;

		shmid = shmget(proKey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		lock3=(int *)memory;

		shmid = shmget(lockKey,sizeof(int),IPC_CREAT|0666);
		memory = shmat(shmid,NULL,0);
		lock1=(int *)memory;
		xchg(lock3);
		xchg(lock1);
		p[*pindex%n]=rand()%100;
		*items=*items+1;
		printf("Producer just update an item, Total items:%d\n",*items);
		chgLock(lock1,0);
		*pindex+=1;
		chgLock(lock3,0);
		sleep(1);
		
		shmdt(items);
		shmdt(p);

		i++;
	}
	exit(0);
}

void ConsumerFun(){
	
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
}
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

	retval = shmdt(p);
	shmdt(cindex);
	shmdt(pindex);
	shmdt(items);
	shmdt(producerindex);

	
	thread thread2(ConsumerFun);
	thread thread1(ProducerFun);
	thread thread3(ConsumerFun);
	thread thread4(ProducerFun);
	thread1.join();
	thread2.join(); 
	thread3.join();
	thread4.join(); 
}
