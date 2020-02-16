#include <stdio.h>
#include<iostream>
#include <pthread.h>
#include <semaphore.h>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h> 
#include <stdlib.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include <sys/types.h>
#include<bits/stdc++.h>
#include<cstring>
const char *semName = "asdfsd";
const char *producerkey="adsbsd";
const char *consumerkey="fdghfh";
key_t cindexkey=(key_t)54348732645;
key_t pindexkey=(key_t)1324365278734;
key_t itemkey=(key_t)13267665432;
key_t buffkey=(key_t)123456123;
key_t lockKey=(key_t)457447547;
key_t proKey=(key_t)55555464;
key_t conskKey=(key_t)65664656;

int n=5;
void* memory = NULL;
int *p,*cindex,*pindex,*items,*producerindex,*lock1,*lock2,*lock3;
int shmid,shmid1,shmid2,shmid3, retval;

int xchg(int* lock){
        int val = 1;
        do{
                __asm__("xchg %0, %1" : "+q" (val), "+m" (*lock));
        }while(val - (*lock) == 0);
        return 0;
}
void chgLock(int *l,int v){
	*l=v;
}
void ConsumerWait(){
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

void ProducerWait(){
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