from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interact.views import LikeViewSet, CollectViewSet, SeenHistoryViewSet, CommentViewSet, RateViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'like', LikeViewSet)
router.register(r'collect', CollectViewSet)
router.register(r'history', SeenHistoryViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'rate', RateViewSet)
router.register(r'follow', FollowViewSet)
urlpatterns = [
    path('interact/', include(router.urls))
]