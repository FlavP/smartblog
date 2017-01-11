from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def redir(request):
    path = reverse('blog_article_list')
    return HttpResponseRedirect(path)