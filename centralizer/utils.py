from django.shortcuts import render, redirect

class ViewObjectsMixin:
    form_object = None
    template = ''
    
    def get(self, request):
        return render(request, self.template, {'theform': self.form_object()})
    
    def post(self, request):
        bounded = self.form_object(request.POST)
        if bounded.is_valid():
            saved_form = bounded.save()
            return redirect(saved_form)
        else:
            return render(request, self.template, {'theform': self.form_object()})