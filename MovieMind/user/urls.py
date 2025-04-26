from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.userinfo_views import CustomUserViewSet

router = DefaultRouter()
router.register(r'userinfo', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # 挂router
]
