from django.urls import include, path
from rest_framework import routers

from . import views, viewsets


router = routers.DefaultRouter()
router.register(r'users', viewsets.AccountAuthViewSet)
router.register(r'register', viewsets.AccountRegisterViewSet)

urlpatterns = [
    path('', include(router.urls))
]
