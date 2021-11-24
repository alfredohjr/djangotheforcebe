'''
    Criado por: Alfredo Holz Junior
    Email: alfredo@jacomarsm.com.br ou alfredojrgasper@gmail.com
    
    Objetivo do script: Script com alguns serviços de envio de email,
        o metodo mais versatil criado até agora é o "envia_email_V4";
        mas os outros não devem ser alterados nem deletados, pois são
        legados :)
        
    Melhorias:
'''

import mimetypes
import os
import shutil
import smtplib
from dotenv import dotenv_values
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from job.core.log.logger import setup_logger

log = setup_logger('core')

config = dotenv_values()


class Mail:

    def __init__(self):
        self.admin_email = config.get('admin_email')
        self.admin_pass = config.get('admin_pass') 
        self.email_port = config.get('email_port') 
        self.email_serv = config.get('email_serv')  
        self.email_from = config.get('email_from')
        self.attach = None
        log.info('email started')

    def add_attach(self,message, filename):
        if not os.path.isfile(filename):
            raise Exception(filename + ' not found')

        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            with open(filename) as f:
                mime = MIMEText(f.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(filename, 'rb') as f:
                mime = MIMEImage(f.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(filename, 'rb') as f:
                mime = MIMEAudio(f.read(), _subtype=subtype)
        else:
            with open(filename, 'rb') as f:
                mime = MIMEBase(maintype, subtype)
                mime.set_payload(f.read())

            encoders.encode_base64(mime)

        mime.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(mime)

    def sendV2(self,attach,to,title,message):
        
        log.info('started')
        self.originalAttachPath = attach

        try:
            shutil.copy(attach,'.')
        except:
            log.error('error to copy attach to ' + os.getcwd())

        fil = str.split(attach,'/')[-1]

        self.attach = fil

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        if type(to) == list:
            msg['To'] = ', '.join(to)
        else:
            msg['To'] = ', '.join([to])
        msg['Subject'] = title

        msg.attach(MIMEText(message.replace('\n','<br>'), 'html', 'utf-8'))

        self.add_attach(msg, self.attach)

        raw = msg.as_string()

        smtp = smtplib.SMTP_SSL(self.email_serv, self.email_port)
        smtp.login(self.email_from, self.admin_pass)
        smtp.sendmail(self.email_from, to, raw)
        smtp.quit()
        log.info('finished')

    def sendV3(self,to,title,message):

        log.info('started')
        if type(to) != list:
            to = list([to])

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = ', '.join(to)
        msg['Subject'] = title

        msg.attach(MIMEText(message.replace('\n','<br>'), 'html', 'utf-8'))

        raw = msg.as_string()

        smtp = smtplib.SMTP_SSL(self.email_serv, self.email_port)
        smtp.login(self.email_from, self.admin_pass)
        smtp.sendmail(self.email_from, to, raw)
        smtp.quit()
        log.info('finished')

    def send(self,title,message,attach=None,to=None):
        '''
        Função para substituir os metodos envia_email_V3 e envia_email_V2
        Anexo pode ser informado ou não
        se o parametro para não for informado, a mensagem é enviada para
        o admin do serviço, definido no arquivo conf, parametro admin_email
        '''
        
        if (attach) and (to):
            self.sendV2(attach,to,title,message)
        elif (attach) and (to == None):
            self.sendV2(attach,to=self.admin_email,title=title,message=message)
        elif (attach == None) and (to):
            self.sendV3(to=to,title=title,message=message)
        elif (attach == None) and (to == None):
            self.sendV3(to=self.admin_email,title=title,message=message)
        else:
            pass
            
        try:
            if self.attach:
                os.remove(self.attach)
                os.remove(self.originalAttachPath)
        except:
            log.error('Error to delete files: ' + self.attach + ', ' +self.originalAttachPath)
        log.info('email finished')
            