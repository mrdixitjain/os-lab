// critical section problem for three entities
// searcher, deleter and inserter.

// done by Dixit Kumar Jain
// date : march 29, 2020



#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

struct Node {
	int value;
	struct Node* next;
};

int searchers = 0;
int inserters = 0;
sem_t delete, insert, search, S, I, mulInsert; 
// mulInsert -> multiple insert. will make insertion mutually exclusive.
// S will keep searchers isolated i.e. only one process can access it one time.
// I will keep access to inserters exclusive.

struct Node *head;
struct Node *tail;

void printList() {
	struct Node *temp;
	temp = head;
	while(temp != NULL && temp->next != NULL) {
		printf("%d->", temp->value);
		temp = temp->next;
	}

	if(temp!=NULL)
		printf("%d\n", temp->value);
}


void* inserter(void *args) {
	sem_wait(&I);
	inserters+=1;
	if(inserters == 1){
		sem_wait(&insert); // lock the insert so deleter or other inserter can't enter.
	}
	sem_post(&I);

	// critical section
	sem_wait(&mulInsert); // no other inserter is allowed to be in cs except current.
	// sleep(2);
	printf("inserter in\n");

	// insertion operation.
	struct Node *a;
	a = (struct Node *)malloc(sizeof(struct Node));
	a->value = rand()%100; // random value will be inserted.
	a->next = NULL;
	printf("%d inserted in the list.\n", a->value);
	if(head == NULL){
		head = a;
		tail = head;
	}
	else {
		tail->next = a;
		tail = a;
	}

	printf("inserter out\n");
	sem_post(&mulInsert);

	sem_wait(&I);
	inserters--;
	if(inserters == 0) {
		sem_post(&insert);
	}
	sem_post(&I);
}

void *deleter(void *args) {
	// first take mutual exclusion.

	sem_wait(&search); // lock the search so no searcher can enter.
	sem_wait(&insert); // lock the insert so no inserter can enter.
	sem_wait(&delete); // lock the delete so no other deleter can enter.
	
	printf("deleter in\n");

	// critical section

	int k = rand()%100; // random value to be deleted if found.

	// deletion operation.

	struct Node *temp = head;
	struct Node *prev = NULL;
	while(temp!=NULL && temp->value != k) {
		prev = temp;
		temp = temp->next;

	}

	if(temp!=NULL) {
		if(prev != NULL) {
			prev->next = temp->next;
		}
		else {
			head = head->next;
		}
		free(temp);
		printf("%d deleted from list\n", k);
	}
	else {
		printf("%d does not exist in list, so can't be deleted\n", k);
	}

	printf("deleter out\n");

	// release all the locks.
	sem_post(&delete);
	sem_post(&insert);
	sem_post(&search);
} 

void *searcher(void *args) {
	sem_wait(&S); // first lock the S so no other process can access searchers
	if(searchers == 0){
		sem_wait(&search); // lock the search so no deleter can enter until there is any searcher processing.
		// sem_wait(&delete);
	}
	searchers += 1; // update searchers
	sem_post(&S); // release SI
	printf("searcher in\n");

	// critical section

	int k = rand()%100; // random generated number to be searched.

	// search operation.
	struct Node *temp = head;
	while(temp!=NULL && temp->value != k) {
		temp = temp->next;
	}

	if(temp!=NULL) {
		printf("%d found in list\n", k);
	}
	else {
		printf("%d does not exist in list\n", k);
	}

	printf("searcher out\n");


	sem_wait(&S); // lock the S so no other process can access searchers
	searchers -= 1; // update searchers
	if(searchers == 0)
		sem_post(&search); // release the search if no more searchers processing.
	sem_post(&S); // release SI
}

int main() {

	// initialize all semaphores

	sem_init(&delete, 0, 1);
	sem_init(&insert, 0, 1);
	sem_init(&search, 0, 1);
	sem_init(&S, 0, 1);
	sem_init(&I, 0, 1);
	sem_init(&mulInsert, 0, 1);
	
	// int a=0, b=0, c=0;

	srand(time(0));

	head = NULL;
	tail = NULL;

	pthread_t pid[100];
	int i = 0;

	while(i<100) {
		// printf("hello\n");
		int k = rand()%3+1;
		switch(k) {
			case 1:
				pthread_create(&pid[i], NULL, inserter, NULL); // thread for inserter
				i++;
				// a++;
				break;
			case 2:
				pthread_create(&pid[i], NULL, deleter, NULL); // thread for deleter
				i++;
				// b++;
				break;
			case 3:
				pthread_create(&pid[i], NULL, searcher, NULL); // thread for searcher
				i++;
				// c++;
				break;
		}
		printList();
	}

	for(int k = 0; k<100; k++)
		pthread_join(pid[k], NULL);

	sem_destroy(&search);
	sem_destroy(&insert);
	sem_destroy(&delete);
	sem_destroy(&S);
	sem_destroy(&I);
	sem_destroy(&mulInsert);
	// printf("%d %d %d\n", a, b, c);
}