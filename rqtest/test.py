from hotqueue import HotQueue
from job import Job
from threading import Thread
import time


job = Job()
t = Thread(target=job.run)
t.setDaemon(True)
t.start()
print 'haha'

time.sleep(3)
job.report()

#t.join()
print "finish"
