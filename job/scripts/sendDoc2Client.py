import requests
import pdfkit
import datetime
from django.core.mail import EmailMessage

from shop.models.Document import Document
from shop.models.DocumentFolder import DocumentFolder
from job.core.log.logger import setup_logger

log = setup_logger('sendDoc2Client')

class Request:

    def __init__(self,baseUrl):
        self.baseUrl = baseUrl
        self.token = 'Token b8e577fa9c296c7c0a49e98272eb636c44d5996f'
        self.header = {'Authorization':self.token}

    def get(self, url):
        return requests.get(self.baseUrl + url, headers=self.header)

    def post(self, url):
        return requests.post(self.baseUrl + url, headers=self.header)


def run():

    queryset = Document.objects.all()
    folder = DocumentFolder.objects.filter(isActive=True, order=True, documentType='OUT')

    queryset = queryset.filter(folder__in=folder)
    queryset = queryset.filter(isOpen=False)
    queryset = queryset.filter(deletedAt=None)
    queryset = queryset.filter(sendMail=True)
    queryset = queryset.exclude(entity__email=None)

    if queryset:
        req = Request('http://localhost:8000')
        for doc in queryset:
            now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            pdfDoc = f'tmp/document_{doc.id}{now}.pdf'
            res = req.get(f'/shop/sale/document/{doc.id}/')
            pdfkit.from_string(res.text,pdfDoc)

            message = EmailMessage(
                'Olá',
                'Esse é um exemplo de documento',
                'documento@example.com',
                ['alfredojrgasper@gmail.com']
            )

            message.attach_file(pdfDoc)
            message.send()

            doc = Document.objects.get(id=doc.id)
            doc.sendMail = False
            doc.save()