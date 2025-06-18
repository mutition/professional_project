
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from interact.models import Like, Collect, Rate, Comment
from .models import Movie, MovieTag


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
        comments = Comment.objects.filter(movie=movie,visible=True)
        comment_list = []
        for comment in comments:
            comment_list.append({
                "comment_id": comment.id,
                "comment_content": comment.content,
                "comment_likes": comment.likes,
                "comment_updated_time": comment.updated_time,
                "user_name" : comment.user.username,
                "user_id" : comment.user.id,
                "user_avatar" : comment.user.avatar,
            })
        return Response({"comment_list": comment_list})




class MovieRecommendViewSet(GenericViewSet):
    queryset = Movie.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        movie_list = []

        # 根据用户 tag 随机获取对应 Movie
        for tag in user.tag:
            tag_movies = MovieTag.objects.filter(tag=tag).order_by('?')[:2]
            for movie_tag in tag_movies:
                movie_list.append(movie_tag.movie)

        # 去重
        unique_movies = list(set(movie_list))

        # 不分页
        serializer = MovieSerializer(unique_movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='top_movie')
    def top_movie(self, request):
        top_movies = Movie.objects.order_by('-like_count')[:100]
        serializer = MovieSerializer(top_movies, many=True)
        return Response(serializer.data)




