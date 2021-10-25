from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    objetos = models.Manager()

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objetos.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objetos.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_update = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    objetos = models.Manager()

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    objetos = models.Manager()

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
