import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm as BSUserCreationForm
from django.contrib.auth import get_user_model
from .utils import ActivationMailFormMixin

logger = logging.getLogger(__name__)


class UserCreationForm(BSUserCreationForm, ActivationMailFormMixin):

    class Meta(BSUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
        mail_validation_error = ('User created. Could not send email to activate account')

        def save(self, **kwargs):
            user = super().save(commit=False)
            if not user.pk:
                user.is_active = False
                send_mail = True
            else:
                send_mail = False
            user.save()
            #save many-tomany relations
            self.save_m2m()
            if send_mail:
                self.send_mail(user=user, **kwargs)
                return user

class ResendActivationEmailForm(ActivationMailFormMixin, forms.Form):
    email = forms.EmailField()

    mail_validation_error = ('Couldn\'t resent activation email, please try again later')
    
    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=self.cleaned_data['emil'])
        except:
            logger.warning("The user with email {} does not exist".format(self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user