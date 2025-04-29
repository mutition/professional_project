from django.urls import path, include
from rest_framework.routers import DefaultRouter

from adm.views import AdminMovieViewSet, AdminUserViewSet, AdminCommentViewSet

router = DefaultRouter()
router.register(r'movie', AdminMovieViewSet)
router.register(r'user',AdminUserViewSet)
router.register(r'comment', AdminCommentViewSet)
urlpatterns = [
    path('admin/', include(router.urls))
]