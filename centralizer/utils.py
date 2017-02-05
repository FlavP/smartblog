from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured

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

class CreateViewForm(View:

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