#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
using namespace std;

static int *tickets;
static bool *choosing;
static int *val;
static int *processNo;
# define N 5

// To calculate the value of max ticket that the current process will get
int maxValue(){
	int m = INT_MIN;
	for(int i=0;i<N;i++){
		if(tickets[i]>m)
			m=tickets[i];
	}
	return m;
}


void initialiseTickets(){
	tickets = (int*)malloc(sizeof(int)*1000);
	memset((void*)tickets, 0, sizeof(tickets)); 
}




void startProcess(int x){
	choosing[x]=true;
	tickets[x]= maxValue()+1;
	choosing[x]=false;
	int i=0;
	// ALL PROCESSES PERFORM THIS
	for(i=0;i< N;i++){
		if(i==x)
			continue;
		while(choosing[i])
			 sleep(6);
		while(tickets[i]!=0 && tickets[i]<tickets[x])
			 sleep(6);
		if(tickets[i]==tickets[x] && i<x){
			while(tickets[i]!=0)
				 sleep(6);
		}

	}
	cout<<"\nprocess "<<x+1<<" is in critical section"<<endl;
	// CRITICAL SECTION
	*val = *val + 15;
	cout<<"Updated value after the execution of process"<<x<<": value = "<<*val<<endl;
	cout<<"\nprocess "<<x<<" is out of critical section"<<endl;
	tickets[x]=0;
}

int main(){

	initialiseTickets();
	choosing = (bool*)malloc(sizeof(bool)*N); 
	val = (int*)malloc(sizeof(int)*N);
	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	choosing = static_cast<bool*>(mmap(NULL, sizeof *choosing*N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	tickets = static_cast<int*>(mmap(NULL, sizeof *tickets*N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	processNo = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	//initial shared memory allocation
	*val = 10;
	*processNo=1;
	int process_no;
	for(int i=0;i<N;i++){
	int pid=fork();
	
	if(pid<0){
		cout<<"Processes are not created"<<endl;
		exit(0);
	}
	else if(pid==0){
		process_no=*processNo;
		*processNo=*processNo+1;
		startProcess(process_no);
	}
	else{
		process_no=*processNo;
		*processNo=*processNo+1;
		startProcess(process_no);
	}
}
	return 0;
}