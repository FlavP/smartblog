from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as toka_toka
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

class ActivationMailFormMixin:
    mail_validation_error = ''

    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError('Cannot set mail_sent attribute.')

    #practic in get_message, iau din argumente numele template-ului si variabilele din context si le renderizez
    #pentru a vedea ce template folosesc si cu ce parametrii
    def get_message(self, **kwargs):
        email_template_name = kwargs.get('email_template_name')
        context = kwargs.get('context')
        return render_to_string(email_template_name, context)

    #ceva similar facem si in get_subject
    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get('subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(subject_template_name, context)
        #subject *must not* contain new lines
        subject = ''.join(subject.splitlines())
        return subject

    #acum construim variabila "context" pentru metodele de mai sus
    def get_context_data(self, request, user, context=None):
        if context is None:
            context = dict()