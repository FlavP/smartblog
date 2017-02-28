from django.shortcuts import get_object_or_404

from .models import Article
from django.views.generic.dates import YearMixin as SecYearMixin, MonthMixin as SecMonthMixin, DateMixin,\
    _date_from_string
from django.http.response import Http404

class GetArticleMixin:
    errors = {'url_kwargs':'We have this {} so the url must be made up by year, month, slug in this order',
              'not_there': 'No {} by this date and slug.'
              }

    def get_object(self, queryset=None):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        slug = self.kwargs.get('art_slug')
        return get_object_or_404(Article, added__year=year, added__month=month, art_slug__iexact=slug)

class YearMixin(SecYearMixin):
    year_query_kwarg = 'year'
    year_url_kwarg = 'year'
    
    def get_year(self):
        year = self.year
        if year is None:
            year = self.kwargs.get(
                self.year_url_kwarg,
                self.request.GET.get(self.year_query_kwarg)
                )
        if year is None:
            raise Http404("No year specified")
        return year
    
class MonthMixin(SecMonthMixin):
    month_format = "%m"
    month_query_kwarg = 'month'
    month_url_kwarg = "month"
    
    def get_month(self):
        month = self.month
        if month is None:
            month = self.kwargs.get(
                self.month_url_kwarg,
                self.request.GET.get(
                    self.month_query_kwarg
                    )
                )
        if month is None:
            raise Http404("There is no month specified")
        return month


class DateObjectMixin(YearMixin, MonthMixin, DateMixin):
    def _make_single_date_lookup(self, date):
        date_field = self.get_date_field()
        if self.uses_datetime_field():
            begin = self._make_date_lookup_arg(date)
            end = self._make_date_lookup_arg(self.get_next_month(date))
            return {
                '%s__gte' % date_field: begin,
                '%s__lt' % date_field: end,
            }
        else:
            return {
                '%s__gte' % date_field: date,
                '%s__lt' % date_field: self.get_next_month(date),
            }

    def get_object(self, queryset=None):
        year = self.get_year()
        month = self.get_month()
        date = _date_from_string(
            year, self.get_year_format(), month, self.get_month_format()
        )
        if queryset is None:
            queryset = self.get_queryset()
        if (not self.get_allow_future() and date > date.today()):
            raise Http404("Future {} is not allowed because {}.allow_future is False").format(
                (queryset.model._meta.verbose_name_plural),
                self.__class__.__name__)
        quer_filter = (self._make_single_date_lookup(date))
        queryset = queryset.filter(**quer_filter)
        return super().get_object(queryset=queryset)
