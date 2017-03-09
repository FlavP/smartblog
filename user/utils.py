from smtplib import SMTPException

from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as toka_toka
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import (BadHeaderError, send_mail)

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
        current = get_current_site(request)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
            token = toka_toka.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
        context.update({
            'domain': current.domain,
            'protocol': protocol,
            'site_name': current.name,
            'token': token,
            'user': user,
            'uid': uid,
        })
        return context

    def _send_mail(self, request, user, **kwargs):
        kwargs['context'] = self.get_context_data(request, user)
        mail_kwargs = {
            'subject': self.get_subject(**kwargs),
            'message': self.get_message(**kwargs),
            'from_email': (settings.DEFAULT_FROMEMAIL),
            'recipient_list': [user.email],
        }
        try:
            no_send = send_mail(**mail_kwargs)
        except Exception as err:
            self.log_email_error(error=err, **mail_kwargs)
            if isinstance(err, BadHeaderError):
                err_type = 'badheader'
            if isinstance(err, SMTPException):
                err_type = 'smtperror'
            else:
                err_type = 'unknow'
            return (False, err_type)

