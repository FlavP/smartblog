from django.shortcuts import get_object_or_404

from .models import Article

from django.http.response import Http404

class GetArticleMixin:

    errors = {'url_kwargs':
              "Generic view {} must be called with "
              "year, month, and slug"}

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        art_slug = self.kwargs.get('art_slug')
        if (year is None or month is None or art_slug is None):
            raise AttributeError(self.errors['url_kwargs'].format(self.__class__.__name__))
        return get_object_or_404(Article, added__year=year, added__month=month, art_slug__iexact=art_slug)
