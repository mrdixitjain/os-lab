#include<bits/stdc++.h>
#include<time.h>
#include<unistd.h>
using namespace std;
int cindex=0,pindex=0,items=0;
int lock1=0;
int lock2=0;
int n=100;
int buff[100]={0};
int j=0;
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
void Consumer(){
	int i=0;
	while(i<15){
		sleep(2);
		while(items<1);
		int consume=buff[(cindex++)%100];
		xchg(&lock1);
		cout<<"Consumer consume an item that is :"<<consume<<" at index :"<<cindex-1<<endl;
		items--;
		cout<<"Total items:"<<items<<endl;
		chgLock(&lock1,0);
		i++;
		}
}
void Producer(){
	int i=0;
	while(i<25){
			sleep(1);
			while(items>99);
			buff[(pindex++)%n]=rand()%100;
			xchg(&lock1);
			cout<<"Producer produce an item that is :"<<buff[(pindex-1)%n]<<" at index :"<<pindex-1<<endl;
			items++;
			cout<<"Total items:"<<items<<endl;
			chgLock(&lock1,0);
			i++;
		}
}
int main(){

	srand(time(0));
	thread thread1(Producer);
	thread thread2(Consumer);
	thread1.join();
	thread2.join();
}
