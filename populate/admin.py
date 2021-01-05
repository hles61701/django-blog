from populate import base
# 原先的資料填充程式是使用預設User model 現在需要改為匯入account App的客製化User model
# from django.contrib.auth.models import User
from account.models import User


def populate():
    print('Creating admin account ... ', end='')
    User.objects.all().delete()
    User.objects.create_superuser(
        username='admin', password='admin', email=None, fullName='管理者')
    print('done')


if __name__ == '__main__':
    populate()
