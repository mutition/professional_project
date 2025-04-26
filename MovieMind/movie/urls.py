from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieView, MovieActionViewSet, MovieCommentViewSet

router = DefaultRouter()
router.register(r'movie', MovieView)
router.register(r'movieaction',MovieActionViewSet,basename='movieaction')
router.register(r'moviecomment',MovieCommentViewSet,basename='moviecomment')
urlpatterns = [
    path('', include(router.urls)),
]