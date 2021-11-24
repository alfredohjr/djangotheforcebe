from django.http import JsonResponse
from rest_framework import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone

from permission.models import Log

class PermissionLog:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if (request.path.find('/admin/') >= 0) \
            or (request.path.find('swagger') > 0) \
            or (request.path.find('/api/token/') >= 0):
            response = self.get_response(request)
            return response

        Authorization = request.headers.get('Authorization')
        if Authorization.split(' ')[0] not in ['Bearer','Token']:
            return JsonResponse({'message':'user not authenticated'}, status=401)

        AuthMethod = Authorization.split(' ')[0]
        auth = None
        if AuthMethod == 'Token':
            auth = authentication.TokenAuthentication()
            auth = auth.authenticate(request)
        elif AuthMethod == 'Bearer':
            auth = JWTAuthentication()
            auth = auth.authenticate(request)

        if auth is None:
            return JsonResponse({'message':'user not authenticated'}, status=401)

        l = Log()
        l.user = auth[0]
        l.url = request.get_full_path()
        l.method = request.method
        l.text = request.body
        l.save()

        Log.objects.filter(pk=l.pk).update(startedAt=timezone.now())
        response = self.get_response(request)
        Log.objects.filter(pk=l.pk).update(finishedAt=timezone.now())

        return response