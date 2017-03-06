from django.shortcuts import get_object_or_404

from .models import Article
from django.views.generic.dates import YearMixin as YearlyMixin, MonthMixin as MonthlyMixin, DateMixin, _date_from_string

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

class AllowFutureArticleMixin():

    def get_future_article(self):
        return self.request.user.has_perm(
            'blog.view_future_article'
        )

class YearMixin(YearlyMixin):
    year_query_kwarg = 'year'
    year_url_kwarg = 'year'

    def get_year(self):
        year = self.year
        if year is None:
            year = self.kwargs.get(
                self.year_url_kwarg,
                self.request.GET.get(
                    self.year_query_kwarg))
        if year is None:
            raise Http404("No year specified")
        return year

class MonthMixin(MonthlyMixin):
    month_query_kwarg = 'month'
    month_url_kwarg = 'month'

    def get_month(self):
        month = self.month
        if month is None:
            month = self.kwargs.get(
                self.month_url_kwarg,
                self.request.GET.get(
                    self.month_query_kwarg))
        if month is None:
            raise Http404("No month is specified")
        return month

class DateObjectMixin(DateMixin, YearMixin, MonthMixin, AllowFutureArticleMixin):

    def get_object(self, queryset=None):
        year = self.get_year()
        month = self.get_month()
        date = _date_from_string(
            year, self.get_year_format(),
            month, self.get_month_format()
        )
        if queryset is None:
            queryset = self.get_queryset()
        if (not self.get_allow_future() and date > date.today()):
            raise Http404(
                "The Future date {} is not available because {}.allow_future is set to False".format(
                    (queryset.model.meta.verbose_name_plural), self.__class__.__name__ ))
        filter_dict = (self._make_single_date_lookup(date))
        queryset = queryset.filter(**filter_dict)
        return super().get_object(queryset=queryset)

    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field()
        if self.uses_datetime_field:
            since = self._make_date_lookup_arg(date)
            until = self._make_date_lookup_arg(self.get_next_month(date))
            return {
                '%s__gt' % date_field: since,
                '%s__lt' % date_field: until,
            }
        else:
            return {
                '%s__gt' % date_field: date,
                '%s__lt' % date_field: self.get_next_month(date)
            }

