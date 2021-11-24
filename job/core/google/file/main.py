
from dotenv import dotenv_values
from job.core.google.main import Create_Service

config = dotenv_values()

class File:

    def __init__(self):
        CLIENT_SECRET_FILE = (config.get('path_scripts') + '/client_secrets.json')
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
        self.service = service
    
    def get(self, file:str, parents:str=None):
        
        page_token = None
        files = []
        while True:
            response = self.service.files().list(q='name="{FILE}"'.format(FILE=file)
                                                , spaces='drive'
                                                , fields='nextPageToken' #, files(id, name)'
                                                , pageToken=page_token).execute()
            for file in response.get('files', []):
                files.append(file)
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        
        if not files:
            return None

        return files


    def create(self,file):
        pass