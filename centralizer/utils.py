from django.shortcuts import render, redirect, get_object_or_404

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

class UpdateObjectsMixin:
    form_object = None
    template = ''
    model = None

    def get(self, request, slug):
        new_obj = get_object_or_404(self.model, slug__iexact=slug)
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
