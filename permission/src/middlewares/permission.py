from django.contrib.auth.models import User
from permission.models import GroupPermission, Permission as PermissionModel, Log, Group, UserGroup

from rest_framework import authentication

from django.shortcuts import HttpResponse, redirect

class Permission(authentication.TokenAuthentication):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        auth = self.authenticate(request)
        response = self.get_response(request)

        # if request.path in ['/admin/login/','/admin/logout/']:
        #     return response

        if request.path.find('/admin/') >= 0:
            return response

        if auth is None:
            return redirect('/admin/login/')

        l = Log()
        l.user = auth[0]
        l.url = request.path
        l.text = request.body
        l.save()

        if request.user.is_superuser:
            print('is superuser')
            return response

        permissionExists = PermissionModel.objects.filter(method=request.method,url=request.path)
        if not permissionExists:
            return HttpResponse('permissao não encontrada')

        groupExists = GroupPermission.objects.filter(permission=permissionExists[0].id)
        if not groupExists:
            return HttpResponse('grupo de permissões não encontrado')

        userPermissionExists = UserGroup.objects.filter(user=auth[0],group=groupExists[0].id)
        if not userPermissionExists:
            return HttpResponse('Você não tem acesso a esse recurso')


        return response