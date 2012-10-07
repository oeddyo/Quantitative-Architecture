from rq import Connection, Queue
from mycount import get_100
from redis import Redis
import time


# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue('low',connection=redis_conn, async=True)  # no args implies the default queue

# Delay calculation of the multiplication
#job = q.enqueue(get_words, 'http://google.com')
job = q.enqueue(get_100, 'ha')
print dir(job)
print job.is_finished
print job.is_failed
print job.result   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print job.result   # => 889

