import ast
import re

from django.core.management.base import BaseCommand

from input.models import CollectMovieDB
from movie.models import Movie, MovieTag


class Command(BaseCommand):
    help = '删除 ratings_count 小于 10000 的数据'

    def handle(self, *args, **options):
        add_list = []
        for movie in Movie.objects.all():
            tags_list = ast.literal_eval(movie.tags)
            for tag in tags_list:
                movietag=MovieTag(movie=movie, tag=tag)
                add_list.append(movietag)
        MovieTag.objects.bulk_create(add_list)


