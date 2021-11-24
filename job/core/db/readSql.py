import os
from pandas import read_sql
from dotenv import dotenv_values
from sqlalchemy import create_engine
import datetime as dt

from job.core.log.logger import setup_logger

log = setup_logger('core')

class sqltodf:

    def __init__(self,banco):
        log.debug('started')
        log.debug('db:' + banco)

        config = dotenv_values()

        self.path_more = config.get('path_more')

        try:
            self.banco = config.get('db_' + banco.lower())
        except Exception as e:
            self.banco = None
            log.error('error:' + str(e))
        
        if self.banco == None:
            raise Exception('banco de dados ' + banco + ' invalido.')

        tipo, usuario, senha, instancia = self.banco.split(',')
        if tipo == 'oracle':
            eng = 'oracle+cx_oracle://{USER}:{PASS}@{SID}'.format(USER=usuario,PASS=senha,SID=instancia)
            self.eng = create_engine(eng)
            log.debug('eng:' + eng)

        os.environ['NLS_LANG'] = "AMERICAN_AMERICA.WE8ISO8859P1"

        self.data = dt.datetime.now().strftime('%Y%m')

    
    def execute(self,sql):
        log.debug('started sql')
        log.debug('sql: ' + sql)
        df = read_sql(sql,self.eng)
        log.debug('total lines:' + str(df.index.size) + ' X ' + str(len(df.keys())))
        log.debug('finished sql')

        try:
            f = open(self.path_more + '/LOG_f_sqltodf_{}.log'.format(self.data),'a')
            f.write(dt.datetime.now().strftime('<sql><data>[%d/%m/%y %H:%M:%S]</data><sqlcommand>') + sql + '</sqlcommand><sql>\n')
            f.close()
        except:
            f = open(self.path_more + '/LOG_f_sqltodf_{}.log'.format(self.data),'a')
            f.write(dt.datetime.now().strftime('<sql><data>[%d/%m/%y %H:%M:%S]</data><sqlcommand>') + sql + '</sqlcommand></sql>\n')
            f.close()
        return df

    def executeFromFile(self,file,params):
        '''
        le um arquivo sql e retorna um dataframe,
        aceita um dicionario de parametros.
        '''

        sql = ''
        with open(file,'r') as file:
            sql = file.read()

        if params == None:
            return self.execute(sql)
        else:
            return self.execute(sql.format(**params))
