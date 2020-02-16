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
key_t cindexkey=(key_t)54348732645;
key_t pindexkey=(key_t)1324365278734;
key_t itemkey=(key_t)13267665432;
key_t buffkey=(key_t)123456123;
int n=5;
void* memory = NULL;
int *p,*cindex,*pindex,*items;
int shmid,shmid1,shmid2,shmid3, retval;

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