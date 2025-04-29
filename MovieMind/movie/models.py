
from django.db import models


class Movie(models.Model):

    name = models.CharField(max_length=255,default='')
    large_images = models.TextField(default='')
    small_images = models.TextField(default='')
    director = models.CharField(max_length=255,default='')
    actors = models.TextField(default='')
    countries = models.CharField(max_length=1000, default='')
    aka = models.CharField(max_length=1000, default='')
    tags = models.CharField(max_length=1000,default='')
    language = models.CharField(max_length=100,default='')
    durations = models.TextField(default='')
    pubdate = models.CharField(max_length=1000, default='')
    rating = models.FloatField(null=True)
    summary = models.TextField(default='')
    like_count = models.IntegerField(null=True)

    # 添加一个显示名称的方法
    def __str__(self):
        return self.name

class MovieTag(models.Model):
    movie = models.ForeignKey(Movie, to_field="id", on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, db_index=True, blank=True, null=False)