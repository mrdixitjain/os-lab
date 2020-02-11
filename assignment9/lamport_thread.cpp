#include<bits/stdc++.h>
#include<unistd.h>
#include<sys/mman.h>
#include<thread>
using namespace std;

#define N 10 //no of threads

bool choosing[N];

int tickets[N];
thread tid[N];

static int *val;

//int val=4;

int maxValue(){
	return *max_element(tickets,tickets+N);
}


void init(){
	for(int i=0;i<N;i++){
		tickets[i]=0;
	}
}


void Process(int x){

	choosing[x]=true;
	tickets[x]=maxValue()+1;
	choosing[x]=false;

	for(int i=0;i<N;i++){
		if(i==x)
			continue;
		while(choosing[i])
			 sleep(4);
		while(tickets[i]!=0 && tickets[i]<tickets[x])
			 sleep(4);
		if(tickets[i]==tickets[x] && i<x){
			while(tickets[i]!=0)
				 sleep(4);
		}

	}

	cout<<"\nprocess "<<x+1<<" is in critical section"<<endl;
	*val=*val+2;
	//val+=2;

	//cout<<"Process "<<x+1<<":val= "<<*val<<endl;
	cout<<"Updated value after the execution of process"<<x+1<<": value = "<<*val<<endl;
	cout<<"\nprocess "<<x+1<<" is out of critical section"<<endl;

	tickets[x]=0;
}

int main(){

	init();

	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

	*val=10;

	for(int i=0;i<N;i++){
		 tid[i]=thread(Process,i);
	}

	for(int i=0;i<N;i++){
		tid[i].join();
	}


	cout<<"final updated value:"<<*val<<endl;

	return 0;
}