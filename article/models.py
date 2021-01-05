from django.db import models
from account.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    pubDateTime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)
    # 多對多欄位，一篇文章可以有許多人按讚，同一個人也可以對多文章按讚

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pubDateTime']


class Comment(models.Model):
    Article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
    pubDateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Article.title + '-' + str(self.id)

    class Meta:
        ordering = ['pubDateTime']
