from sqlalchemy import create_engine
from dotenv import dotenv_values
import os
import datetime as dt

from job.core.log.logger import setup_logger

config = dotenv_values()
log = setup_logger('core')

class Execsql:
    '''
    Executa uma funcao dentro do banco, funciona com
    insert, update, delete e etc; procedures e coisas
    mais complexas não.
    '''

    def __init__(self,db):
        log.debug('started')
        log.debug('db:' + db)

        self.db = ''
        try:
            self.db = config.get('db_' + db.lower())
        except Exception as e:
            self.db = None
            log.error('error:' + str(e))
        
        if self.db == None:
            raise Exception('banco de dados ' + db + ' invalido.')

        tipo, usuario, senha, instancia = self.db.split(',')
        if tipo == 'oracle':
            eng = 'oracle+cx_oracle://{USER}:{PASS}@{SID}'.format(USER=usuario,PASS=senha,SID=instancia)
            self.eng = eng
            log.debug('eng:' + eng)

        os.environ['NLS_LANG'] = "AMERICAN_AMERICA.WE8ISO8859P1"

        self.date = dt.datetime.now().strftime('%Y%m')


    def execute(self,command):

        con = create_engine(self.eng)
        con.execute(command)