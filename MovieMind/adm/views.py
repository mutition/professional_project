from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import serializers, mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from interact.models import Comment
from movie.models import Movie

User = get_user_model()

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class AdminMovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','date_joined']

class AdminUserViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

class AdminCommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    pagination_class = LimitOffsetPagination
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        data = []
        for comment in page:
            movie = comment.movie
            user = comment.user
            data.append({
                'comment_id': comment.id,
                'movie_id': movie.id,
                'movie_name': movie.name,
                'user_name': user.username,
            })
        return self.get_paginated_response(data)

    @action(detail=True, methods=['get'])
    def visible(self, request, pk=None):
        comment = self.get_object()
        comment.visible = True
        comment.save()
        return Response({"status": "success", "visible": comment.visible})








