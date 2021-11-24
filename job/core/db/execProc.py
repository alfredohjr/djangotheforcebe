from sqlalchemy import create_engine
import cx_Oracle
from dotenv import dotenv_values
import os
import datetime as dt

from job.core.log.logger import setup_logger

config = dotenv_values()
log = setup_logger('core')

class ExecProc:

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
            eng = '{USER}/{PASS}@{SID}'.format(USER=usuario,PASS=senha,SID=instancia)
            self.eng = eng
            log.debug('eng:' + eng)

        os.environ['NLS_LANG'] = "AMERICAN_AMERICA.WE8ISO8859P1"

        self.date = dt.datetime.now().strftime('%Y%m')    

    def execute(self,procedure,paramsIn,paramsOut=None):
        '''
        Funcao usada para executar procedures no banco de dados oracle.
        Para parametros de saida utilize para NUMBER = cx_Oracle.NUMBER e 
        VARCHAR = cx_Oracle.NCHAR.
        
        Para a variavel de entrada para_in utilize uma turple somente de
        caracteres.
        
        Para a variavel de entrada para_out faca o seguinte: crie variaveis
        para char ou number, depois de criadas coloque-as em uma lista e informe
        no paramentro.
        
        E retornado a saida da procedure, provavelmente com o nome do arquivo.
        
        Exemplo:
        banco = 'prdrac'
        procedure = 'PROC_VARRDIAX'
        para_in = ['1','0','044064','0','0','0','1180601','1180620','B','A','N','G','G','N','N','0','N']
        
        var1 = '0'
        var2 = 0.
        para_out = [var1,var2]
        
        saida = f_execproc(banco = 'prdrac',para_in = para_in, para_out = para_out, procedure = procedure)
        '''
        
        nl = []

        engg = cx_Oracle.connect(self.eng)
        cur = engg.cursor()

        para_n = []

        if paramsOut != None:

            for i in paramsOut:
                if type(i) == str:
                    nl.append(cur.var(cx_Oracle.NCHAR))
                elif type(i) == int:
                    nl.append(cur.var(cx_Oracle.NUMBER))
                elif type(i) == float:
                    nl.append(cur.var(cx_Oracle.NUMBER))
                else:
                    print('A variavel {} é do tipo {} que não foi convertida, pode ocorrer erro na execucao!'.format(i,type(i)))
        
            para_n = paramsIn + nl

        else:
            para_n = paramsIn

        res = cur.callproc(procedure
                    ,para_n)
        
        cur.close()
        engg.close()
        
        return res