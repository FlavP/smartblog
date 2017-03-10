from django.contrib.auth.forms import UserCreationForm as BSUserCreationForm
from .utils import ActivationMailFormMixin

class UserCreationForm(BSUserCreationForm, ActivationMailFormMixin):

    class Meta(BSUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
        mail_validation_error = ('User created. Could not send email to activate account')

        def save(self, **kwargs):
            user = super().save(commit=False)