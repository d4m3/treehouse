from rest_framework import routers

from . import viewsets



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
