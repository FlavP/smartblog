from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

class ContactUs(forms.Form):
    
    email = forms.EmailField(
        initial = 'flaviuspopoiu@gmail.com')
    body = forms.CharField(widget=forms.Textarea)
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    REASON_CHOICES = (
        (FEEDBACK, "Feedback"),
        (CORRECTION, "Corection"),
        (SUPPORT, "Support"),
        )
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        initial=FEEDBACK
        )
    
    def send_email(self):
        reason = self.cleaned_data.get('reason')
        reason_dict = self.cleaned_data.get(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        body = "Message From: {}\n\n{}\n".format(email, text)
        try:
            #shortcut for send_email
            mail_managers(full_reason, body)
        except BadHeaderError:
            self.add_error(
                None,
                ValidationError(
                    'Could not send email.\n'
                    'Extra Headers not allowed '
                    'in email body.',
                    code='badheader'))
            return False
        else:
            return True