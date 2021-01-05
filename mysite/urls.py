"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from main import views


# urlpatterns : diango利用python的串列資料結構來儲存各個URL的對應
# 每個URL對應利用path()或re_path()來設定
urlpatterns = [
    # 如果URL格式為admain/..，admin.site.urls模組進一步比對URL，此為Django內建管理者模組
    path('admin/', admin.site.urls),

    path('account/', include('account.urls', namespace='account')),

    # 第二組階段比對
    path('article/', include('article.urls', namespace='article')),

    # 如果URL格式為main/..，main.urls模組第三階段比對，空間名稱main
    path('main/', include('main.urls', namespace='main')),

    # re是正規表示法'.*'任何字元任何字
    re_path('.*', views.main)
]
