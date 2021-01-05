from django.contrib import admin
from article.models import Article, Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['Article', 'content', 'pubDateTime']  # 讓清單顯示2+1欄位
    list_display_links = ['Article']  # 設定資料連結欄位
    list_filter = ['Article', 'content']  # 點選文章標題就會列出所屬留言
    search_fields = ['content']  # 出現搜尋欄位
    list_editable = ['content']  # 可以直接編輯content欄位內容

    class Meta:
        model = Comment


admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)
