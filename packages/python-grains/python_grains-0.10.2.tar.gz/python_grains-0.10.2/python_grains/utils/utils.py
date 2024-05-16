import redis
from redis.retry import Retry
from redis.backoff import DecorrelatedJitterBackoff
import socket
import time
import datetime
import pytz
import logging

class RedisClientWithRetry(object):

    @classmethod
    def from_config(cls, *args, max_retry=5, **kwargs):
        backoff = DecorrelatedJitterBackoff(cap=2.0, base=0.5)
        retry = Retry(retries=max_retry, backoff=backoff)
        redis_client = redis.Redis(*args,
                                   retry_on_error=[redis.exceptions.ConnectionError,
                                                   redis.exceptions.TimeoutError,
                                                   socket.timeout],
                                   retry=retry,
                                   **kwargs)
        return redis_client

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def search_obj_from_array(array, fieldname, fieldvalue):
    _obj = [o for o in array if o.get(fieldname, str(fieldvalue) + 'not_it') == fieldvalue]
    if len(_obj) == 0:
        return None
    return _obj[0]


class Timer(object):

    def __init__(self, name=None, info=None, logger=None, logger_name='timings', sub=False):

        self.start = time.time()
        self.end = None
        self.timings = []
        self.info = info
        self.logger = logger or logging.getLogger(logger_name)
        self.sub = sub
        self.name = name or 'timer'

    def subtimer(self, name, info=None):
        t = Timer(name=name, info=info, logger=self.logger, sub=True)
        self.timings.append(t)
        return t


    def register(self, name, info=None):

        assert self.end is None, 'This timer instance is already done'
        assert name != 'total', 'Name cannot be `total`'

        self.timings.append((time.time(), name, info))

    def done(self, send_log=True, loglvl='info', logverbose=True):

        self.end = time.time()
        self.timings = sorted(self.timings, key=lambda x: x.start if isinstance(x, Timer) else x[0])

        if send_log and not self.logger is None:
            getattr(self.logger, loglvl)('Timing done', extra=self.result(verbose=logverbose))

    def result(self, verbose=True):

        if self.end is None:
            self.done(send_log=False)

        durations = [x[1]-x[0] for x in zip([self.start, *self.timings[:-1]], self.timings)]

        if verbose:

            timings = [{
                'name': x[1],
                'time': pytz.utc.localize(datetime.datetime.utcfromtimestamp(x[0])).isoformat(),
                'info': x[2],
                'duration': duration
            } for x, duration in zip(self.timings, durations)]

            r = {
                'start': pytz.utc.localize(datetime.datetime.utcfromtimestamp(self.start)).isoformat(),
                'end': pytz.utc.localize(datetime.datetime.utcfromtimestamp(self.end)).isoformat(),
                'duration': self.total,
                'info': self.info,
                'timings': timings}

        else:

            r = {
                x[1]: duration
                for x, duration in zip(self.timings, durations)}
            r.update({'total': self.total})

        return r

    @property
    def total(self):
        return self.end - self.start


