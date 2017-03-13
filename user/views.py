from django.shortcuts import render
from django.contrib.auth import get_user, logout, get_user_model, logout
from django.utils.encoding import force_text
from django.contrib.messages import error, success
from django.contrib.auth.tokens import default_token_generator as def_token
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse_lazy
from .forms import UserCreationForm, ResendActivationEmailForm
from .utils import MailContextViewMixin
from django.views.generic import View


#TemplateResponse is usually used in Auth instead of HttpResponse
class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = ('user/user_confirm_delete.html')
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = ('user/user_confirm_delete.html')

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request):
        return TemplateResponse(request, self.template_name)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        user = get_user(request)
        user.set_unusable_password()
        user.is_active = False
        user.save()
        logout()
        return redirect(self.success_url)

class CreateAccount(MailContextViewMixin, View):

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})

    #for the post method we use a special decorator for sensitive information, like passwords, so they won't be displayed
    #in the event of an error log or something
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password', 'password_confirm'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            bound_form.save(**self.get_save_kwargs(request))
        if bound_form.mail_sent:
           return redirect(self.succress_url)
        else:
            error = (bound_form.non_field_errors())
            for er in error:
                error(request, er)
                return redirect('dj-auth:resend_activation')
        return TemplateResponse(self.template_name, {'form': bound_form})

class ActivateAccount(View):
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/user_activate.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_encode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user=None
        if (user is not None and def_token.check_token(user, token)):
            user.is_active = True
            user.save()
            success(request, 'User is active, login')
            return redirect(self.success_url)
        else:
            return TemplateResponse(request, self.template_name)
        
class ResendActivationEmail(MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/resend_activation.html'
    
    @method_decorator(csrf_protect)
    def get(self, request):
        #forma clasica, bine ar fi s-o memorezi un pic
        return TemplateResponse(request, self.template_name, {'form': self.form_class})
    
    @method_decorator(csrf_protect)
    def post(self, request):
        #bounduim formularul, iar ar fi bine s-o stii pe asta
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(**self.get_save_kwargs(request))
            success(request, 'Activation Email Sent')
            return redirect(self.success_url)
        if (user is not None and not bound_form.mail_sent):
            err = (bound_form.non_field_errors())
            for er in err:
                error(request, er)
            if err:
                bound_form.errors.pop('__all__')
        return TemplateResponse(request, self.template_name, {'form': bound_form})
        
        
        
    




