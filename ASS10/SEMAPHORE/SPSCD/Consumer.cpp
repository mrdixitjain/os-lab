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

	
	*cindex+1;

	sem_t *sem_id = sem_open(semName, O_CREAT, 0600, 0);
    if (sem_id == SEM_FAILED){
        perror("Consumer  : [sem_open] Failed\n");
        exit(0);
    }
	if (sem_wait(sem_id) < 0)
		printf("Consumer wait for update item\n");
	shmid = shmget(itemkey,sizeof(int),IPC_CREAT|0666);
	memory = shmat(shmid,NULL,0);
	items=(int *)memory;
	*items=*items-1;
	sleep(.9);
	printf("Consumer just update an item, Total items:%d\n",*items);
	shmdt(cindex);
	shmdt(items);
	sem_post(sem_id);
	i++;
}
exit(0);
}