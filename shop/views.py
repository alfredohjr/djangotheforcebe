from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML

from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Product import Product
from shop.models.Price import Price

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


def createSaleDocument(request,document_id):

    document = Document.objects.get(id=document_id)
    documentProduct = DocumentProduct.objects.filter(document=document)

    obj = {}
    obj['document'] = document
    obj['entity'] = document.entity
    obj['deposit'] = document.deposit
    obj['documentProduct'] = documentProduct
    return render(request, 'sale.html', obj)


def reportProduct(request):

    obj = {}
    queryset = Product.objects.all()

    obj['products'] = queryset
    return render(request, 'reportProduct.html', obj)


def reportPrice(request):

    obj = {}
    queryset = Price.objects.all()
    queryset = queryset.order_by('deposit__name','product__name','-startedAt')
    queryset = queryset.filter(isValid=True)
    queryset = queryset.filter(Q(finishedAt__gte=timezone.now()) | Q(finishedAt=None))
    queryset = queryset.filter(Q(startedAt__lte=timezone.now()) | Q(finishedAt=None))
    queryset = queryset.exclude(startedAt=None)
    

    if request.GET.get('tipo'):
        tipo = request.GET.get('tipo')
        queryset = queryset.filter(priceType=tipo)
    
    if request.GET.get('inicio'):
        inicio = request.GET.get('inicio')
        queryset = queryset.filter(startedAt=inicio)

    valid = []
    validIndex = []
    for q in queryset:
        if [q.deposit,q.product] not in valid:
            valid.append([q.deposit,q.product,q.priceType])
            validIndex.append(q.id)

    queryset = queryset.filter(id__in=validIndex)
    queryset = queryset.order_by('deposit__name','product__name','startedAt')
    obj['prices'] = queryset
    return render(request, 'reportPrice.html', obj)