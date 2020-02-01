import sys

from updateInput import *
from updateOutput import *
from printOutput import *

# SOURCE: collaborated with John Gauthier
#         implementation ideas largely from Danny Yoo of UC Berkley on hashcollision.org

class RedBlackTree:

    class Node():
        def __init__(self, process, key=None, color='red'):
            self.right = None
            self.left = None
            self.p = None
            self.process=process
            self.key = key
            self.color = color

    def __init__(self):
        self.NIL = self.Node(key = None, process=None, color='black')
        self.root = self.NIL
        self.size = 0
        self.ordered = []
        pass

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.p = x
        y.p = x.p
        if x.p == self.NIL:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.p = x
        y.p = x.p
        if x.p == self.NIL:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def insert(self, z):
        new_node = self.Node(process=z, key = z['vruntime'])
        self._insert(new_node)
        self.size += 1

    def _insert(self, z):
        y = self.NIL
        x = self.root
        while x != self.NIL:

            y = x
            if z.key < x.key :
                x = x.left
            else:
                x = x.right
        z.p = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = self.NIL
        z.right = self.NIL
        z.color = "red"
        self.rb_insert_fixup(z)

    def rb_insert_fixup(self, z):
        i = 0
        while z.p.color == "red":
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.color == 'red':
                    z.p.color = "black"
                    y.color = "black"
                    z.p.p.color = "red"
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self.right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.color == 'red':
                    z.p.color = "black"
                    y.color = "black"
                    z.p.p.color = "red"
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = 'black'
                    z.p.p.color = 'red'
                    self.left_rotate(z.p.p)
            i += 1
        self.root.color = 'black'

    def transplant(self, u, v):
        if u.p == self.NIL:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def remove(self, z):
        if self.size == 0:
            print("TreeError")
            return
        our_node = self.key_search(z)
        self._remove(our_node)
        self.size -= 1

    def _remove(self, z):
        y = z
        original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.right)
        else:
            y = self._min_node(z.right)
            original_color = y.color
            x = y.right
            if y.p == z:
                x.p = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if original_color == 'black':
            self.rb_delete_fixup(x)

    def rb_delete_fixup(self, x):
        while x != self.root and x.color == 'black':
            if x == x.p.left:
                w = x.p.right
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == 'red':
                    w.color = 'black'
                    x.p.color = 'red'
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.p
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.p)
                    x = self.root
        x.color = 'black'

    def search(self, x):
        return self._search(self.root, x)

    def _search(self, current_node, target):
        if current_node == self.NIL:
            return "NotFound"
        elif target == current_node.key:
            return "Found"
        elif target < current_node.key:
            return self._search(current_node.left, target)
        else:
            return self._search(current_node.right, target)

    def key_search(self, target):
        return self._key_search(self.root, target)

    def _key_search(self, current_node, target):
        if current_node == self.NIL:
            return None
        elif target.key == current_node.key:
            if(target.process['pid']==current_node.process['pid']):
                return current_node
            # if target.process['pid']==current_node.process['pid']:
                
            else:
                return self._key_search(current_node.left, target)
        elif target.key < current_node.key:
            return self._key_search(current_node.left, target)
        else:
            return self._key_search(current_node.right, target)

    def maximum(self):
        if self.size == 0:
            return "Empty"
        return self._maximum(self.root)

    def _maximum(self, x):
        while x.right != self.NIL:
            x = x.right
        return x.key

    def minimum(self):
        if self.size == 0:
            return "none"
        return self._minimum(self.root)

    def _minimum(self, x):
        while x.left != self.NIL:
            x = x.left
        z=x.process
        self.remove(x)
        return z

    def min(self):
        if self.size == 0:
            return "none"
        return self._min(self.root)

    def _min(self, x):
        while x.left != self.NIL:
            x = x.left
        z=x.process
        return z

    def _min_node(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def inprint(self):
        if self.size == 0:
            print("Empty")
            return
        self._inprint(self.root)
        for i in range(len(self.ordered)-1):
            print(self.ordered[i], end=' ')
        print(self.ordered[-1])
        self.ordered = []

    def _inprint(self, x):
        if x != self.NIL and x.key != None:
            self._inprint(x.left)
            self.ordered.append(x.process['pid'])
            self._inprint(x.right)

def updateOutput(outputQueue, rb, outputRunning, time, endedProcess, inputQueue): # to update outputQueue[] i.e. to check if any process has done it's work on output devices or if not than decrease it's time by 1.
    if(len(outputQueue)<=0):
        outputRunning.append('idle')
        return
    # print(ioQueue[0]['execution'])
    if(int(outputQueue[0]['execution'][1])>0):
        outputRunning.append(outputQueue[0]['pid'])
        outputQueue[0]['execution'][1]=str(int(outputQueue[0]['execution'][1])-1)
        if(outputQueue[0]['execution'][1]=="0"):
            outputQueue[0]['execution']=outputQueue[0]['execution'][2:]
            if(len(outputQueue[0]['execution'])>0):
                if(outputQueue[0]['execution'][0]=='P'):
                    if(rb.size>0):
                        a=rb.min()
                        outputQueue[0]['vruntime']=a['vruntime']
                    rb.insert(outputQueue[0])
                elif(outputQueue[0]['execution'][0]=='O'):
                    outputQueue.append(outputQueue[0])
                else:
                    inputQueue.append(outputQueue[0])
            else:
                outputQueue[0]['endTime']=time
                endedProcess.append(outputQueue[0])
            del outputQueue[0]



def updateInput(inputQueue, rb, inputRunning, time, endedProcess, outputQueue): # to update inputQueue[] i.e. to check if any process has done it's work on input devices or if not than decrease it's time by 1.
    if(len(inputQueue)<=0):
        inputRunning.append('idle')
        return
    # print(ioQueue[0]['execution'])
    if(int(inputQueue[0]['execution'][1])>0):
        inputRunning.append(inputQueue[0]['pid'])
        inputQueue[0]['execution'][1]=str(int(inputQueue[0]['execution'][1])-1)
        if(inputQueue[0]['execution'][1]=="0"):
            inputQueue[0]['execution']=inputQueue[0]['execution'][2:]
            if(len(inputQueue[0]['execution'])>0):
                if(inputQueue[0]['execution'][0]=='P'):
                    if(rb.size>0):
                        a=rb.min()
                        inputQueue[0]['vruntime']=a['vruntime']
                    rb.insert(inputQueue[0])
                elif(inputQueue[0]['execution'][0]=='O'):
                    outputQueue.append(inputQueue[0])
                else:
                    inputQueue.append(inputQueue[0])
            else:
                inputQueue[0]['endTime']=time
                endedProcess.append(inputQueue[0])
            del inputQueue[0]



def CFS(rb):
    currRunTime=0
    # to store processes executing or waiting for input output devices
    inputQueue=[]
    outputQueue=[]

    # to keep track of processes running on cpu, input and output device.
    # here, index will work as time unit.
    cpuRunning=[]
    inputRunning=[]
    outputRunning=[]

    endedProcess=[]# keep track of all processes which completed their execution.

    # all resources will stay idle till first process will arrive.
    time=0
    currentProcess='none'
    currentProcess=rb.minimum()
    if(currentProcess!='none'):
        if(currentProcess['startTime']==-1):
            currentProcess['startTime']=time

    while(currentProcess!='none' or rb.size>0 or len(inputQueue)>0 or len(outputQueue)>0):
        # print("-> ", end="")
        # print(currentProcess)
        # print()
        # print(inputQueue)
        # print()
        # print(outputQueue)
        # print()
        # print(endedProcess)
        # print()
        # rb.inprint()
        # print()
        updateInput(inputQueue, rb, inputRunning, time, endedProcess, outputQueue)
        updateOutput(outputQueue, rb, outputRunning, time, endedProcess, inputQueue)
        time+=1
        if(currentProcess!="none"):
            if(len(currentProcess['execution'])>0):
                if(currentProcess['execution'][0]=='P'): # i.e. it was working on cpu last.
                    if(int(currentProcess['execution'][1])>0):
                        cpuRunning.append(currentProcess['pid'])
                        currentProcess['execution'][1]=str(int(currentProcess['execution'][1])-1)
                        currRunTime+=1

                    if(int(currentProcess['execution'][1])==0): # if it's current execution on cpu is finished.
                        currentProcess['execution']=currentProcess['execution'][2:]
                        if(len(currentProcess['execution'])>0): # i.e. process is not completed yet.
                            if(currentProcess['execution'][0]=='I'): # will go for input
                                currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
                                # to complete current cycle of updateInput.
                                inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
                            if(currentProcess['execution'][0]=='O'):
                                # to complete current cycle of updateOutput.
                                currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
                                outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
                            # now another process will run on cpu.
                            currRunTime=0
                            currentProcess=rb.minimum()
                            if(currentProcess!='none'):
                                if(currentProcess['startTime']==-1):
                                    currentProcess['startTime']=time
                        
                        else: # process is completed. Add it to endedProcess[] and check for new process to run on cpu
                            currentProcess['endTime']=time
                            endedProcess.append(currentProcess)

                            # if there is a process to run on cpu than ok else currentProcess = "none"
                            currRunTime=0
                            currentProcess=rb.minimum()
                            if(currentProcess!='none'):
                                if(currentProcess['startTime']==-1):
                                    currentProcess['startTime']=time
                    elif(currRunTime>=currentProcess['slice']):
                        currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
                        rb.insert(currentProcess)
                        currRunTime=0
                        currentProcess=rb.minimum()
                        if(currentProcess!='none'):
                            if(currentProcess['startTime']==-1):
                                currentProcess['startTime']=time

                else: # if current process is using input or output device
                    cpuRunning.append('idle')
                    currentProcess['vruntime']+=(1024/currentProcess['weight'])*currRunTime
                    if(currentProcess['execution'][0]=='I'): # will go for input
                        # to complete current cycle of updateInput.
                        inputQueue.append(currentProcess) # process added to inputQueue where it'll wait for it's turn.
                    if(currentProcess['execution'][0]=='O'):
                        # to complete current cycle of updateOutput.
                        outputQueue.append(currentProcess) # process added to outputQueue where it'll wait for it's turn.
                    # now another process will run on cpu if there is any.
                    currRunTime=0
                    currentProcess=rb.minimum()
                    if(currentProcess!='none'):
                        if(currentProcess['startTime']==-1):
                            currentProcess['startTime']=time
        else: # check if there is any process processes to run.
            cpuRunning.append('idle')
            currRunTime=0
            currentProcess=rb.minimum()
            if(currentProcess!='none'):
                if(currentProcess['startTime']==-1):
                    currentProcess['startTime']=time

    # print('end')
    # print(endedProcess)
    return endedProcess

if __name__=="__main__":
    rb=RedBlackTree()
    file = open('cfs.dat', 'r')
    data = file.readlines()
    schedLatency=int(data[0])
    minGranularity=int(data[1])
    weights=[88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916, 9548, 7620, 6100, 4904, 3906, 3121, 2501, 1991, 1586, 1277,
    1024, 820, 655, 526, 423, 335, 272, 215, 172, 137, 110, 87, 70, 56, 45, 36, 29, 23, 18, 15]
    processes=[]
    totalWeight=0
    for i in range(2, len(data)):
        processes.append({})
        process=data[i].split()
        processes[i-2]['pid']=int(process[0])
        processes[i-2]['niceness']=int(process[1])
        processes[i-2]['weight']=weights[int(process[1])+20]
        totalWeight+=processes[i-2]['weight']
        processes[i-2]['execution']=process[2:len(process)-1]
        processes[i-2]['startTime']=-1
        processes[i-2]['endTime']=-1
        processes[i-2]['totalBurst']=0
        processes[i-2]['vruntime']=0
        j=3
        while(j<len(process)):
            if(process[j-1]=='P'):
                processes[i-2]['totalBurst']+=int(process[j])
            j+=2
    for i in processes:
        i['slice']=max((i['weight']/totalWeight)*schedLatency, minGranularity)
        rb.insert(i)
    answer=CFS(rb)
    printOutput(answer, "CFS")