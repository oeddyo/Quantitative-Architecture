import time
import multiprocessing
class Job(multiprocessing.Process):
    def __init__(self):
        self.cur_time = 0
        pass
    def run(self):
        for i in range(10):
            self.cur_time+=1
            time.sleep(1)
        return True
    def report(self):
        print self.cur_time
        #return self.cur_time

"""
def slow_fib(n):
    if n <= 1:
        return 1
    else:
        return slow_fib(n-1) + slow_fib(n-2)

"""
