from django.shortcuts import render, redirect, get_object_or_404
from article.models import Article, Comment
from article.forms import ArticleForm
from django.contrib import messages
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required  # 限制權限使用函數
from main.views import admin_required  # 限制只有管理者使用

# Create your views here.


def article(request):
    '''
    Render the article page
    '''

    # articles = Article.objects.all()
    # 取出所有的文章，Django 稱查詢出來的資料為查詢集(Query set)

    articles = {article: Comment.objects.filter(
        Article=article) for article in Article.objects.all()}
    # 將articles 變數改為一個dict K:V=文章:留言
    context = {'articles': articles}
    # 利用範本變數article將查詢集至範本，修改範本以顯示文章資料在context區塊加到內容
    return render(request, 'article/article.html', context)


@admin_required
def articleCreate(request):
    '''
    Create a new article instance
        1. If method is GET, render an empty form
        2. If method is POST,
            * vaildate the form and display error message if the form is invalid
            * else , save it to the model and redirect to the article page
    '''

    # # TODO: finish the code
    # return render(request, 'article/article.html') # 測試

    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        # print(ArticleForm()) 可以看到表單預設結構是table
        return render(request, template, {'articleForm': ArticleForm()})

    # POST
    articleForm = ArticleForm(request.POST)

    # 如果驗證錯誤
    if not articleForm.is_valid():
        return render(request, template, {'articleForm': articleForm})

    articleForm.save()
    # return article(request)
    messages.success(request, '文章已新增')
    return redirect('article:article')  # 轉向到article


def articleRead(request, articleId):
    '''
    Read an article
        1. Get the article instance; redirect to the 404 page if not found
        2. Render the articleRead template with the article instance and its associated comments
    '''
    article = get_object_or_404(Article, id=articleId)
    context = {
        'article': article,
        # 'comments': Comment.objects.filter(article=article)
        'comments': Comment.objects.filter(Article=article)
    }
    return render(request, 'article/articleRead.html', context)


@admin_required
def articleUpdate(request, articleId):
    '''
    Update the article instance:
        1. Get the article to update; redirect to 404 if not found
        2. If method is GET, render a bound form
        3. If method is POST,
            * vaildate the form and render a bound form if the form is invalid
            * else, save it to the model and redirect to the article page
    '''
    # # TODO: finish the code
    # return render(request, 'article/article.html') 測試
    article = get_object_or_404(Article, id=articleId)
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, template, {'articleForm': articleForm})

    # POST
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm': articleForm})

    articleForm.save()
    messages.success(request, '文章已修改')
    return redirect('article:articleRead', articleId=articleId)


# ------文章刪除---------
@admin_required
def articleDelete(request, articleId):
    '''
    Delete the article instance:
        1. Render the article page if the method is GET
        2. Get the article to delete; redirect to 404 if not found
    '''
    if request == 'GET':
        return render('article:article')

    # POST
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, '文章已刪除')
    return redirect('article:article')


# ------文章搜尋---------
def articleSearch(request):
    '''
    Search for articles:
        1. Get the "searchTerm" from the HTML form
        2. Use "searchTerm" for filtering
    '''
    searchTerm = request.GET.get('searchTerm')
    articles = Article.objects.filter(
        Q(title__icontains=searchTerm) | Q(content__icontains=searchTerm))

    context = {'articles': articles, 'searchTerm': searchTerm}
    return render(request, 'article/articleSearch.html', context)


# ------文章按讚---------
@login_required
def articleLike(request, articleId):
    '''
    Add the user to the 'like' field:
        1. Get the article; redirect to 404 if not found
        2. If the user does not exist in the "like" field, add him/her
        3. Finally, call articleRead() funtion to render the article
    '''
    article = get_object_or_404(Article, id=articleId)
    if request.user not in article.likes.all():
        article.likes.add(request.user)
    return articleRead(request, articleId)


# ------文章留言板---------
@login_required
def commentCreate(request, articleId):
    '''
    Create a comment for an article:
        1. Get the "comment" from the HTML form
        2. Store it to database
    '''
    if request.method == 'GET':
        return articleRead(request, articleId)

    # POST
    comment = request.POST.get('comment')
    if comment:
        comment = comment.strip()
    if not comment:
        return redirect('article:articleRead', articleId=articleId)

    article = get_object_or_404(Article, id=articleId)
    Comment.objects.create(
        Article=article, user=request.user, content=comment)
    return redirect('article:articleRead', articleId=articleId)


# ------文章留言修改---------
@login_required
def commentUpate(request, commentId):
    '''
    Update a comment:
        1. Get the comment to update and its article; redirect to 404 if not found
        2. If it is a 'GET' request, return
        3. If the comment's author is not the user, return
        4. If comment is empty, delete the comment, else update the comment
    '''
    commentToUpdate = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=commentToUpdate.Article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)

    # POST
    if commentToUpdate.user != request.user:
        messages.error(request, '無修改權限')
        return redirect('article:articleRead', articleId=article.id)

    comment = request.POST.get('comment', '').strip()  # 刪除舊留言
    if not comment:
        commentToUpdate.delete()
        # 如果沒有留言內容就刪除整篇留言
    else:
        commentToUpdate.content = comment
        commentToUpdate.save()
    return redirect('article:articleRead', articleId=article.id)


# ------文章留言刪除---------
@login_required
def commentDelete(request, commentId):
    '''
    Delete a comment:
        1. Get the commet to update and its article; redirct to 404 if not found
        2. If it is a 'GET' request, return
        3. If the comment's author is not the user, return
        4. Delete the comment
    '''
    comment = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=comment.Article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)

    # POST
    if comment.user != request.user:
        messages.error(request, '無刪除權限')
        return redirect('article:articleRead', articleId=article.id)

    comment.delete()
    return redirect('article:articleRead', articleId=article.id)
