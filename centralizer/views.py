from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template import Context, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect, reverse
from .forms import TagForms, CompanyForms, NewsForm
from django.views.generic import View, DetailView, DeleteView, ListView, CreateView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
#from .utils import ViewObjectsMixin, UpdateObjectsMixin, DeleteObjectMixin, ViewDetails, CreateViewForm
from .models import RelatedNews
# Create your views here.
#we are already in centralizer, so we don't need call centralizer.models
from .models import Tag, Company
from django.urls.base import reverse_lazy
from core.utils import UpdateView
from .utils import PageLinksMixin, GetRelatedObjectMixin, CompanyMixin #RelatedFormMixin
from user.decorators import custom_login_required, require_authenticated_permission, class_login_required

@require_authenticated_permission(
    'centralizer.add_relatednews')
class RelatedNewsCreate(GetRelatedObjectMixin, CompanyMixin, CreateView):
    form_class = NewsForm
    model = RelatedNews

    def get_initial(self):
        company_slug = self.kwargs.get(
            self.company_slug_url_kwarg)
        self.company = get_object_or_404(
            Company, slug__iexact=company_slug)
        initial = {
            self.company_context_object_name:
                self.company,
        }
        initial.update(self.initial)
        return initial


@require_authenticated_permission(
    'centralizer.delete_relatednews')
class RelatedNewsDelete(
        GetRelatedObjectMixin,
        CompanyMixin,
        CreateView):
    form_class = NewsForm
    model = RelatedNews
    slug_url_kwarg = 'related_slug'

    def get_success_url(self):
        return (self.object.company
                .get_absolute_url())


@require_authenticated_permission(
    'centralizer.change_relatednews')
class RelatedNewsUpdate(
        GetRelatedObjectMixin,
        CompanyMixin,
        CreateView):
    form_class = NewsForm
    model = RelatedNews
    slug_url_kwarg = 'related_slug'


@require_authenticated_permission(
    'centralizer.add_company')
class CompanyCreate(CreateView):
    form_class = CompanyForms
    model = Company


@require_authenticated_permission(
    'company.delete_company')
class CompanyDelete(DeleteView):
    model = Company
    success_url = reverse_lazy(
        'centralizer_company_list')


class CompanyDetail(DetailView):
    model = Company


class CompanyList(PageLinksMixin, ListView):
    model = Company
    paginate_by = 5  # 5 items per page


@require_authenticated_permission(
    'centralizer.change_company')
class CompanyUpdate(UpdateView):
    form_class = CompanyForms
    model = Company


@require_authenticated_permission(
    'centralizer.add_tag')
class TagCreate(CreateView):
    form_class = TagForm
    model = Tag


@require_authenticated_permission(
    'centralizer.delete_tag')
class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy(
        'centralizer_tag_list')


class TagDetail(DetailView):
    model = Tag


class TagList(PageLinksMixin, ListView):
    paginate_by = 5
    model = Tag


@require_authenticated_permission(
    'centralizer.change_tag')
class TagUpdate(UpdateView):
    form_class = TagForms
    model = Tag