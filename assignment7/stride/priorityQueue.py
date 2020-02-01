# A simple implementation of Priority Queue 
# using Queue. 
class PriorityQueue(object): 
	def __init__(self): 
		self.queue = [] 

	def __str__(self): 
		return ' '.join([str(i) for i in self.queue]) 

	# for checking if the queue is empty 
	def isEmpty(self): 
		return len(self.queue) == [] 

	# for inserting an element in the queue 
	def insert(self, data): 
		self.queue.append(data) 
		self.queue=sorted(self.queue, key=lambda i: i['pass'])[:]

	# for popping an element based on Priority 
	def delete(self, i):
		if(i<len(self.queue)):
			print(self.queue[i]) 
			del self.queue[i]
		else:
			print('index out of bound.')
