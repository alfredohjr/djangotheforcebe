from threading import Thread, Semaphore
import os
import sys
import subprocess

from job.core.log.logger import setup_logger

sem = Semaphore(10)

log = setup_logger('thread')
logError = setup_logger('thread[error]')

env = {
    **os.environ,
    'PYTHONPATH': os.getcwd()
}

class Th():

    def __init__(self,i):
        self.script = i
        log.info('started:' + i)

    def run(self):

        try:
            sem.acquire()
            sub = subprocess.check_output('python scripts/' + self.script, env=env, stderr=subprocess.STDOUT)
            log.info('process ' + self.script + ' success')
            sem.release
        except subprocess.CalledProcessError as e:
            logError.error(e.output)

        sys.stdout.flush()