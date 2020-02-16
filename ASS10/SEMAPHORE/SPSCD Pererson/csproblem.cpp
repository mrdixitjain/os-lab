#include<bits/stdc++.h>
#include<cstring>
#include<cstdlib>
#include<unistd.h>
#include<sys/ipc.h>
#include<sys/shm.h>
#include <sys/types.h>
#define shmSeg ftok("shmfile",65)
using namespace std;
struct data
{
	int buff[100];
	int cindex=0;
	int pindex=0;
	int items=0;
};
int main(){
	void *shared_memory = (void *)0;
	struct data *data1;
	cout<<"HELLO YASH"<< endl;
	
	int shmid=shmget(shmSeg,sizeof(struct data), 0666| IPC_CREAT );
	if (shmid < 0)
    {
        perror("semget(semid)");
        return -1;
    } 

	shared_memory = shmat(shmid,(void *)0,0);

	if (shared_memory == (void *)-1) {
        fprintf(stderr, "shmat failed\n");
        exit(EXIT_FAILURE);
    }
    printf("Memory attached at %X\n", (int *)shared_memory);

    data1=(struct data *)shared_memory;
    struct data ab=*data1;
    cout<<ab.pindex<<"\t"<<ab.cindex<<endl;
    for(int i=0;i<100;i++){
    	//cout<<ab.buff[i]<<"\t";
    	ab.buff[i]=rand()%20;
    }
    struct data cd=*data1;
    for(int i=0;i<100;i++){
    	cout<<cd.buff[i]<<"\t";
    }
	shmdt(shared_memory);
}
