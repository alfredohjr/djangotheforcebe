import os
import subprocess
import datetime
import sys

sys.path.append(os.getcwd())

from job.core.log.logger import setup_logger

path_scripts = 'job/scripts'

log = setup_logger('execTask')

env = {
    **os.environ,
    'PYTHONPATH': os.getcwd()
}

def f_main():

    id = 0
    di = {}
    for i in os.listdir(path_scripts):
        if i.endswith('.py'):
            print(id,'->',i)
            id += 1
            di[id] = i

    id_t = input('Digite o codigo da tarefa! ')
    log.info('usuario ' + os.getlogin() + ' solicitou a tarefa ' + di.get(int(id_t) + 1) + ' de forma manual.')
    log.info('start task:' + di.get(int(id_t) + 1))
    subprocess.run(['python',path_scripts + '/' + di.get(int(id_t) + 1)],env=env)
    log.info('end task:' + di.get(int(id_t) + 1))

if __name__ == '__main__':
    f_main()