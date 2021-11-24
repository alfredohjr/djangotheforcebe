from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML

from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct

# Create your views here.

def createOrder(request,document_id):

    document = Document.objects.get(id=document_id)
    documentProduct = DocumentProduct.objects.filter(document=document)

    obj = {}
    obj['document'] = document
    obj['entity'] = document.entity
    obj['deposit'] = document.deposit
    obj['documentProduct'] = documentProduct

    html_string = render_to_string('order.html', obj)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    html.write_pdf('tmp/order.pdf')

    fs = FileSystemStorage('tmp')
    with fs.open('order.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response