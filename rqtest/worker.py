from hotqueue import HotQueue
from job import Job
import multiprocessing
import time
queue = HotQueue("myqueue", host="localhost", port=6379, db=0)


while True:
    job = queue.get()
    if job is None:
        time.sleep(1)
        continue
    #d = multiprocessing.Process(name='do_work',target=job.do_job())
    #d.daemon = True
    job.run()
    #d.start()
    job.report()

e = queue.get()
print e
job = Job()
queue.put(job)

print dir(queue)
w = queue.get()
print w
