from django.db import models

class Comment(models.Model):
    movie = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class Collect(models.Model):
    movie = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class Rate(models.Model):
    movie = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    rate = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class Like(models.Model):
    movie = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

class SeenHistory(models.Model):
    movie = models.ForeignKey('movie.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    follower = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='followers')
    created_time = models.DateTimeField(auto_now_add=True)