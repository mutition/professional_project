from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet

from interact.models import Like, Comment, Collect, SeenHistory, Rate
from movie.models import Movie

User = get_user_model()
class LikeViewSet(GenericViewSet):

    queryset = Like.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': '请提供movie_id'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(id=movie_id)
        like_obj ,_ = Like.objects.get_or_create(user=user, movie=movie)

        return Response({
            'like_id': like_obj.id,
            'message': '已喜欢'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            like = Like.objects.get(pk=pk, user=user)
        except Like.DoesNotExist:
            return Response({'error': '未喜欢'}, status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response({'message': '取消喜欢成功'}, status=status.HTTP_204_NO_CONTENT)

    #查找用户点赞列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('movie')

        page = self.paginate_queryset(queryset)

        data = []
        for like in page:
            movie = like.movie
            data.append({
                'like_id': like.id,
                'movie_id': movie.id,
                'movie_name': movie.name,
                'movie_director': movie.director,
                'movie_image': movie.small_images,
            })
        return self.get_paginated_response(data)

class CollectViewSet(GenericViewSet):

    queryset = Collect.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Collect.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': '请提供movie_id'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(id=movie_id)
        collect_obj,_ = Collect.objects.get_or_create(user=user, movie=movie)

        return Response({
            'collect_id': collect_obj.id,
            'message': '已收藏'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            collect = Collect.objects.get(pk=pk, user=user)
        except Collect.DoesNotExist:
            return Response({'error': '未收藏'}, status=status.HTTP_404_NOT_FOUND)
        collect.delete()
        return Response({'message': '取消收藏成功'}, status=status.HTTP_204_NO_CONTENT)

    #查找用户搜藏列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('movie')

        page = self.paginate_queryset(queryset)

        data = []
        for collect in page:
            movie = collect.movie
            data.append({
                'collect_id': collect.id,
                'movie_id': movie.id,
                'movie_name': movie.name,
                'movie_director': movie.director,
                'movie_image': movie.small_images,
            })
        return self.get_paginated_response(data)

class SeenHistoryViewSet(GenericViewSet):

    queryset = SeenHistory.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SeenHistory.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': '请提供movie_id'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(id=movie_id)
        # 查询是否已有历史记录
        history_obj = SeenHistory.objects.filter(user=user, movie=movie).first()
        if history_obj:
            # 已经有了，更新 update_time
            history_obj.updated_time = timezone.now()
            history_obj.save()
            return Response({
                'message': '更新观看记录时间成功',
                'history_id': history_obj.id,
                'update_time': history_obj.updated_time,
            }, status=status.HTTP_200_OK)
        else:
            # 没有，创建新的历史记录
            history_obj = SeenHistory.objects.create(user=user, movie=movie)
            return Response({
                'message': '新建观看记录成功',
                'history_id': history_obj.id,
                'create_time': history_obj.updated_time,  # 假设 create_time = update_time
            }, status=status.HTTP_201_CREATED)

    #查找用户历史记录列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('movie').order_by('-updated_time')

        page = self.paginate_queryset(queryset)

        data = []
        for history in page:
            movie = history.movie
            data.append({
                'history_id': history.id,
                'movie_id': movie.id,
                'movie_name': movie.name,
                'movie_director': movie.director,
                'movie_image': movie.small_images,
            })
        return self.get_paginated_response(data)

class CommentViewSet(GenericViewSet, mixins.UpdateModelMixin):

    queryset = Comment.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': '请提供movie_id'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(id=movie_id)

        content = request.data.get('content')
        if not content:
            return Response({'error': '请提供content'}, status=status.HTTP_400_BAD_REQUEST)

        comment_obj = Comment.objects.create(user=user, movie=movie, content=content)

        return Response({
            'comment_id': comment_obj.id,
            'comment_content': comment_obj.content,
            'message': '评论创建成功'
        }, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk, user=user)
        except Comment.DoesNotExist:
            return Response({'error': '评论不存在或无权删除'}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response({'message': '删除评论成功'}, status=status.HTTP_204_NO_CONTENT)

    #查找用户评论列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('movie')

        page = self.paginate_queryset(queryset)

        data = []
        for comment in page:
            movie = comment.movie
            data.append({
                'movie_id': movie.id,
                'comment_id': comment.id,
                'comment_content': comment.content,
                'movie_name': movie.name,
                'movie_director': movie.director,
                'movie_image': movie.small_images,
            })
        return self.get_paginated_response(data)

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            comment = Comment.objects.get(pk=pk, user=user)
        except Comment.DoesNotExist:
            return Response({'error': '评论不存在或没有权限修改'}, status=status.HTTP_404_NOT_FOUND)
        new_content = request.data.get('content')
        if not new_content:
            return Response({'error': '请提供新的content内容'}, status=status.HTTP_400_BAD_REQUEST)
        comment.content = new_content
        comment.save()
        return Response({'message': '评论更新成功', 'comment_id': comment.id, 'content': comment.content},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def like(self, request, *args, **kwargs):
        commit_id = request.query_params.get('commit_id')
        commit = Comment.objects.get(id=commit_id)
        commit.likes += 1
        commit.save()
        return Response({
            'commit_id': commit_id,
            'likes': commit.likes,
        })


class RateViewSet(GenericViewSet, mixins.UpdateModelMixin):

    queryset = Rate.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rate.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({'error': '请提供movie_id'}, status=status.HTTP_400_BAD_REQUEST)
        movie = Movie.objects.get(id=movie_id)

        rate = request.data.get('rate')
        if not rate:
            return Response({'error': '请提供rate'}, status=status.HTTP_400_BAD_REQUEST)

        rate_obj,_ = Rate.objects.get_or_create(user=user, movie=movie, rate=rate)

        return Response({
            'rate_id': rate_obj.id,
            'rate': rate_obj.rate,
            'message': '评分创建成功'
        }, status=status.HTTP_201_CREATED)

    #查找用户评分列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('movie')

        page = self.paginate_queryset(queryset)

        data = []
        for rate in page:
            movie = rate.movie
            data.append({
                'movie_id': movie.id,
                'rate_id': rate.id,
                'rate_rate': rate.rate,
                'movie_name': movie.name,
                'movie_director': movie.director,
                'movie_image': movie.small_images,
            })
        return self.get_paginated_response(data)

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            rate = Rate.objects.get(pk=pk, user=user)
        except Rate.DoesNotExist:
            return Response({'error': '评分不存在或没有权限修改'}, status=status.HTTP_404_NOT_FOUND)
        new_rate = request.data.get('rate')
        if not new_rate:
            return Response({'error': '请提供新的rate'}, status=status.HTTP_400_BAD_REQUEST)
        rate.rate = new_rate
        rate.save()
        return Response({'message': '评分更新成功', 'rate_id': rate.id, 'rate': rate.rate},
                        status=status.HTTP_200_OK)