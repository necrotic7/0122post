from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    content = models.TextField('內文')
    creator = models.ForeignKey(User, on_delete = models.PROTECT, verbose_name = '建立者', related_name = 'posts')
    create_at = models.DateTimeField('建立時間', auto_now_add = True)
    update_at = models.DateTimeField('更新時間', auto_now = True)
    likes = models.ManyToManyField(User, related_name = 'liked_posts', blank = True)

    def __str__(self):
        return 'Post create by {}'.format(self.creator.username)


class Commit(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name = '文章', related_name = 'commits')
    content = models.TextField('內文')
    creator = models.ForeignKey(User, on_delete = models.PROTECT, verbose_name = '建立者', related_name = 'commits')
    create_at = models.DateTimeField('建立時間', auto_now_add = True)
    update_at = models.DateTimeField('更新時間', auto_now = True)
    likes = models.ManyToManyField(User, related_name = 'liked_commits', blank = True)

    def __str__(self):
        return 'Post create by {}'.format(self.creator.username)