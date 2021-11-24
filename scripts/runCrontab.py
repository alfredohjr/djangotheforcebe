from job.core.crontab.main import Crontab2Django

def run():
    c = Crontab2Django()
    c.executeCron()