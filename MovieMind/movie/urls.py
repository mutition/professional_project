from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieView, MovieActionViewSet, MovieCommentViewSet, MovieRecommendViewSet

router = DefaultRouter()
router.register(r'movie', MovieView)
router.register(r'movieaction',MovieActionViewSet, basename='movieaction')
router.register(r'moviecomment',MovieCommentViewSet, basename='moviecomment')
router.register(r'myrecommend',MovieRecommendViewSet, basename='myrecommend')
urlpatterns = [
    path('movie/', include(router.urls)),
]