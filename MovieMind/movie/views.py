
from rest_framework import serializers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from interact.models import Like, Collect, Rate, Comment
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieView(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

class MovieActionViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        user=request.user
        movie_id=request.query_params.get('movie_id')
        movie=Movie.objects.get(id=movie_id)
        if Like.objects.filter(user=user, movie=movie).exists():
            is_like=True
        else :
            is_like=False
        if Collect.objects.filter(user=user, movie=movie).exists():
            is_collect=True
        else :
            is_collect=False
        rate = Rate.objects.filter(user=user, movie=movie)
        if rate:
            is_rate=rate.first().rate
        else :
            is_rate=False
        comment_list = []
        for comment in Comment.objects.filter(user=user, movie=movie):
            comment_list.append({
                "comment_id": comment.id,
                "comment_content": comment.content,
                "comment_updated_time": comment.updated_time,
            })
        return Response({
            "is_like": is_like,
            "is_collect": is_collect,
            "is_rate": is_rate,
            "comment_list": comment_list,
        })

class MovieCommentViewSet(GenericViewSet):
    def list(self, request, *args, **kwargs):
        movie_id=request.query_params.get('movie_id')
        movie=Movie.objects.get(id=movie_id)
        comments = Comment.objects.filter(movie=movie)
        comment_list = []
        for comment in comments:
            comment_list.append({
                "comment_id": comment.id,
                "comment_content": comment.content,
                "comment_likes": comment.likes,
                "comment_updated_time": comment.updated_time,
            })
        return Response({"comment_list": comment_list})


