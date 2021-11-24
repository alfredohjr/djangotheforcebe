import apiclient.errors as errors
import os
import pandas as pd
from googleapiclient.http import MediaFileUpload
from dotenv import dotenv_values

config = dotenv_values()

from job.core.google.main import Create_Service
from job.core.google.file.main import File
from job.core.log.logger import setup_logger

log = setup_logger('core')

class Sheet:

    def __init__(self):
        CLIENT_SECRET_FILE = (config.get('path_scripts') + '/client_secrets.json')
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
        self.service = service

    def get(self,file:str,parents:str=None):
        '''
        get file metadata
        '''
        df = File()
        res = df.get(file=file,parents=parents)
        log.debug(res)
        return res

    def create(self,file:str,parents:list=None):
        '''
        create new file
        '''
        if not os.path.exists(file):
            return 0

        if self.get(file=file) is None:

            try:
                file_metadata = {
                    'name': os.path.basename(file)
                    , 'mimeType': 'application/vnd.google-apps.spreadsheet'
                    , 'parents': parents
                }

                media = MediaFileUpload(filename=file, mimetype='text/csv')

                response = self.service.files().create(
                    media_body=media,
                    body=file_metadata
                ).execute()

                return response

            except Exception as e:
                log.error(e)
                return False
        else:
            log.error(file + ' already exists, please, use method update')

    def update(self,file,parents:list=None):
        '''
        update file
        '''
        
        if not os.path.exists(file):
            return 0

        files = self.get(file,parents)

        for f in files:

            try:
                file_id = f.get('id')
                media_body = MediaFileUpload(file, resumable=True)

                updated_file = self.service.files().update(
                    fileId=file_id,
                    body=file,
                    media_body=media_body).execute()
                return updated_file
            except errors.HttpError as e:
                print(e)
                return None

    def delete(self,file,folder):
        '''
        delete file
        '''
        pass