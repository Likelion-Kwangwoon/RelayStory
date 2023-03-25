from django.db import models

# Create your models here.
class Book(models.Model):

    user = models.ForeignKey('user.User',on_delete=models.CASCADE)
    cover = models.IntegerField()
    title = models.TextField(max_length=30)
    object=models.Manager()
class Comment(models.Model):

    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    nickname=models.TextField(max_length=30)
    content=models.TextField(max_length=200)
    object=models.Manager()