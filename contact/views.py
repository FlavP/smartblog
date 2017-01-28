from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.views.generic import View
from .forms import ContactUs
# Create your views here.

class EmailView(View):
    formclass = ContactUs
    template = "contact/contact_form.html"
    
    def get(self, request):
        return render(request, self.template, {"theform": self.formclass()})
    
    def post(self, request):
        bounded_form = self.formclass(request.POST)
        if bounded_form.is_valid():
            send_now = bounded_form.send_mail()
            if send_now:
                success(request, "The message has been sent")
                return redirect('blog_article_list')
            return render(request, self.formclass, {"theform": bounded_form})        
