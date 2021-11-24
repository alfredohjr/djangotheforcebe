from django.urls import path, include

from .views import testRoutes

urlpatterns = [
	path('teste/',testRoutes,name='testroutes'),
]