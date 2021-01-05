from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    fullName = models.CharField(max_length=128)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    # blank:html表單可以不輸入資料
    # null:在資料表中可以空值

    def __str__(self):
        return self.fullName + '(' + self.username + ')'
    # 預設顯示使用者全名加帳號
