import os
import psutil
from psutil import virtual_memory
from threading import Thread,Event



class _CheckMem(Thread):
    
    def __init__(self, event, maxMem, every):
        Thread.__init__(self)
        self.stopped = event
        self.every = every
        self.maxMem = maxMem


    def run(self):
        while not self.stopped.wait(self.every):
            process = psutil.Process(os.getpid())
            curMem = process.memory_info().rss 
            if curMem > self.maxMem:
                print('used to much memory: %s GB' %(curMem/8/1024**3))
                os._exit(1)




class limitMemory(object):
    def __init__(self, maxMemory=None, every=1):
        '''
        maxMemory [GB]
            not not set, set to 50% of avail memory
        every [sec]
        This function starts a subprocess
        which checks memory usage by the current python instance [every] ms
        is [maxMemory] limit is reached raise MemoryError
        
        this this nerving system freezes can be avoided
        '''
        if maxMemory is None:
            mem = virtual_memory()
            maxMemory =  0.5 * mem.total/1024**3
        self.maxMemory = maxMemory
        self.every = every


    def __call__(self, func):
        stopFlag = Event()
        thread = _CheckMem(stopFlag, self.maxMemory*1024**3, self.every)
        thread.setDaemon(True)
        thread.start()
        func()
        stopFlag.set()     


    
if __name__ == '__main__':
    import numpy as np
    from time import sleep
    l = []


    @limitMemory(every=0.1, maxMemory=1)
    def fillMemory():
        n=0
        while n<5000:
            print(1)
            l.append(np.random.rand(1e6))
            sleep(0.05)
            n+=1


