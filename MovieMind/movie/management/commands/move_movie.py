import re

from django.core.management.base import BaseCommand

from input.models import CollectMovieDB
from movie.models import Movie

class Command(BaseCommand):
    help = '删除 ratings_count 小于 10000 的数据'

    def handle(self, *args, **options):
        # 执行删除操作
        new_movie_list = []
        for old_movie in CollectMovieDB.objects.all():
            pattern = r"'average':\s*([\d.]+)"
            rating_match = re.search(pattern, old_movie.rating)

            small_pattern = r"'small':\s*'([^']*)'"
            large_pattern = r"'large':\s*'([^']*)'"

            # 匹配 small 的值
            small_match = re.search(small_pattern, old_movie.images)
            small_value = small_match.group(1).strip() if small_match else None

            # 匹配 large 的值
            large_match = re.search(large_pattern, old_movie.images)
            large_value = large_match.group(1).strip() if large_match else None

            direct_pattern = r"'name':\s*'([^']*)'"
            match = re.search(direct_pattern, old_movie.directors)
            name = match.group(1) if match else None

            act_pattern = r"'name':\s*'([^']*)'"
            # 使用正则表达式查找所有匹配项
            actor = re.findall(act_pattern, old_movie.actor)


            new_movie = Movie(name=old_movie.title,small_images=small_value,large_images=large_value,director=name,actors=actor,
                              countries=old_movie.countries,aka=old_movie.aka,tags=old_movie.genres,language=old_movie.languages
                              ,pubdate=old_movie.pubdate,rating=float(rating_match.group(1)),summary=old_movie.summary,like_count=old_movie.wish_count
                              ,durations = old_movie.durations)
            new_movie_list.append(new_movie)
        Movie.objects.bulk_create(new_movie_list)
