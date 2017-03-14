from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from .models import Company, RelatedNews

class ViewObjectsMixin:
    theformclass = None
    template = ''
    
    def get(self, request):
        return render(request, self.template, {'theform': self.theformclass()})
    
    def post(self, request):
        bounded = self.theformclass(request.POST)
        if bounded.is_valid():
            saved_form = bounded.save()
            return redirect(saved_form)
        else:
            return render(request, self.template, {'theform': self.theformclass()})


class PaginationMixin:
    page_param = 'page'

    def _pagination(self, pag_number):
        return "?{page}={n}".format(page=self.page_param, n=pag_number)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context.get('page_obj')
        if page is not None:
            context.update({'previous_page_url': self.previous_page(page), 'next_page_url': self.next_page(page)})
        return context

    def first_pg(self, page):
        #not to show on first page
        if page.number > 1:
            return self._pagination(1)
        return None

    def previous_page(self, page):
        if (page.has_previous() and page.number > 2):
            return self._pagination(self.previous_page_number())
        return None

    def next_page(self, page):
        last = page.paginator.num_pages
        if (page.has_next() and page.number < last - 1):
            return self._pagination(page.next_page_number())
        return None

    def last_pg(self, page):
        last_page = page.paginator.num_pages
        if page.number < last_page:
            return self._pagination(last_page)
        return None

class UpdateObjectsMixin:
    form_object = None
    template = ''
    model = None

    def get(self, request, slug):
        new_obj = get_object_or_404(self.model, company_slug__iexact=slug)
        context = {
            'theform': self.form_object(instance=new_obj),
            self.model.__name__.lower(): new_obj,
        }
        return render(request, self.template, context)

    def post(self, request, slug):
        new_obj = get_object_or_404(self.model, slug__iexact=slug)
        valid_form = self.form_object(request.POST, instance=new_obj)
        if valid_form.is_valid():
            the_new_object = valid_form.save()
            return redirect(the_new_object)
        else:
            context = {
                "theform": valid_form,
                self.model.__name__.lower: new_obj
            }
            return render(request, self.template, context)

class DeleteObjectMixin:
    model = None
    template = ""
    success = ""
    
    def get(self, request, slug):
        new_obj = get_object_or_404(self.model, slug__iexact = slug)
        context = {self.model__name__.lower(): new_obj}
        return render(request, self.template, context)
    
    def post(self, request, slug):
        new_obj = get_object_or_404(self.model, slug__iexact = slug)
        #nu avem nevoie de redirect, pentru ca stim url-ul
        new_obj.delete()
        return HttpResponseRedirect(self.success)

class ViewDetails(View):
    context_name = ''
    context = ''
    template = ''
    template_end = '_details'
    model = None
    
    def get_context_name(self):
        if self.context_name:
            return self.context_name
        elif isinstance(self.object, Model):
            return self.object._meta.name
        else:
            return None
    
    def get_template(self):
        if self.template:
            return self.template
        return "{application}/{model}{end}.html".format(application=self.object.meta.app_label,
                                                        model=self.object._meta.model_name,
                                                        end=self.template_end
                                                        )
    
    #aici iei numele obiectului pe care il dai in context pentru a fi trimis in template. testezi daca ai obiectul si daca-l ai chemi metooda aia
    #care-ti returneaza numele modelului, pe care il folosesti pe post de cheie de dictionar, cu valoare obiectului
    def get_context(self):
        context = {}
        if self.object:
            context_name = (self.get_context_name())
        if context_name:
            context[context_name] = (self.object)
        return context
    
    def get_object_from_model(self):
        slug = self.kwargs.get('slug')
        if slug is None:
            raise AttributeError("{c} expects {p} parameter from URL pattern".format(c = self.__class__.__name__, p='slug'))
        if self.model:
            obj = self.object._meta.model_name
            if obj == 'RelatedNews':
                composed = 'related_slug'                 
            else:
                composed = obj + '_slug'
            return get_object_or_404(self.model, composed__iexact = slug)
        else:
            raise ImproperlyConfigured("{c} need {a} attribute to work.".format(c = self.__class__.__name__, a="model"))
    
    def get(self, request, **kwargs):
        self.kwargs = kwargs
        self.obj = self.get_object_from_model()
        template = self.get_template()
        context = self.get_context()
        return render(request, self.template, context)         

class CompanyMixin():
    company_slug_url_kwarg = 'company_slug'
    company_context_object_name = 'company'
    
    def get_context_data(self, **kwargs):
        company_slug = self.kwargs.get(self.company_slug_url_kwarg)
        company = get_object_or_404(Company, company_slug__iexact=company_slug)
        context = {
            self.company_context_object_name: company,
            }
        context.update(kwargs)
        return super().get_context_data(**context)

class GetRelatedObjectMixin():
    def get_object(self, queryset=None):
        company_slug = self.kwargs.get(
            self.company_slug_url_kwarg
        )
        news_slug = self.kwargs.get(self.related_news_url_kwarg)
        return get_object_or_404(news_slug__iexact = news_slug ,company_slug__iexact=company_slug)

    def get_context_data(self, **kwargs):
        if hasattr(self, 'company'):
            context = {
                self.company_context_object_name: self.company,
            }
        else:
            company_slug = self.kwargs.get(self.company_slug_url_kwarg)
            company = get_object_or_404(Company,
                                             company_slug__iexact=company_slug
                                             )
            context = {
                self.company_context_object_name: company
            }
            context.update(kwargs)
            return super().get_context_data(**context)

'''
class RelatedFormMixin():

    def form_valid(self, form):
        company = get_object_or_404(Company, company_slug__iexact = self.kwargs.get(self.company_slug_url_kwarg))
        self.object = form.save(company_obj=company)
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            self.company = get_object_or_404(
                Company,
                company_slug__iexact=self.kwargs.get(self.company_slug_url_kwarg)
            )
            data = kwargs['data'].copy()
            data.update({'company': self.company})
            kwargs['data'] = data
            return kwargs
'''

class PageLinksMixin:
    page_kwarg = 'page'

    def _page_urls(self, page_number):
        return "?{pkw}={n}".format(
            pkw=self.page_kwarg,
            n=page_number)

    def first_page(self, page):
        # don't show on first page
        if page.number > 1:
            return self._page_urls(1)
        return None

    def previous_page(self, page):
        if (page.has_previous()
                and page.number > 2):
            return self._page_urls(
                page.previous_page_number())
        return None

    def next_page(self, page):
        last_page = page.paginator.num_pages
        if (page.has_next()
                and page.number < last_page - 1):
            return self._page_urls(
                page.next_page_number())
        return None

    def last_page(self, page):
        last_page = page.paginator.num_pages
        if page.number < last_page:
            return self._page_urls(last_page)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs)
        page = context.get('page_obj')
        if page is not None:
            context.update({
                'first_page_url':
                    self.first_page(page),
                'previous_page_url':
                    self.previous_page(page),
                'next_page_url':
                    self.next_page(page),
                'last_page_url':
                    self.last_page(page),
            })
        return context