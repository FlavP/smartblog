from django.shortcuts import redirect


def redir(request):
    return redirect('blog_article_list')