from django.shortcuts import get_object_or_404

from .models import Article

class GetArticleMixin:
    errors = {'url_kwargs':'We have this {} so the url must be made up by year, month, slug in this order'}
    month_url_kwarg = 'month'
    year_url_kwarg = 'year'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        year = self.kwargs.get(self.year_url_kwarg)
        month = self.kwargs.get(self.month_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if (year is None or month is None or slug is None):
            raise AttributeError(self.errors['url_kwargs'].format(self.__class__.__name__))
        return get_object_or_404(Article, added__year = year, added__month = month, art_slug__iexact = slug)
