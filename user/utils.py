from smtplib import SMTPException
import traceback
import logging
from logging import CRITICAL, ERROR

from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator as toka_toka
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.core.mail import (BadHeaderError, send_mail)
from django.core.exceptions import ValidationError

class ActivationMailFormMixin:
    mail_validation_error = ''
    logger = logging.getLogger(__name__)

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
        else:
            if no_send > 0:
                return (True, None)
            self.log_mail_error(**mail_kwargs)
            return (False, "unkown error")

    def send_mail(self, user, **kwargs):
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = [' ' + line for line in tb]
            self.logger.warning('send_mail was called without request.\nTraceback:\n{}'.format(''.join(tb)))
            self._mail_sent = False
            return self._mail_sent
        self._mail_sent, error = (self._send_mail(request, user, **kwargs))
        if not self._mail_sent:
            self.add_error(None, ValidationError(self.mail_validation_error, code=error))
            return self._mail_sent

    def log_mail_error(self, **kwargs):
        msg_list = [
            'Activation email was not sent. \n',
            'from email: {from_email}\n',
            'subject: {subject}\n',
            'message: {message}\n',
        ]
        recipient_list = kwargs.get('recipient_list', [])
        for reci in recipient_list:
            msg_list.insert(1, 'recipient: {r}\n'.format(r=reci))
        if 'error' in kwargs:
            level = ERROR
            err_msg = (
                'error: {0.__class__.__name}\n'
                'args: {0.args}\n'
            )
            err_info = err_msg.format(kwargs['error'])
            err_msg.insert(1, err_info)
        else:
            level = CRITICAL
        msg = ''.join(msg_list).format(**kwargs)
        self.logger.log(level, msg)

class MailContextViewMixin:
    email_template_name = 'user/email_create.txt'
    subject_template_name = ('user/subject_create.txt')

    def get_save_kwargs(self, request):
        return {
            'email_template_name': self.email_template_name,
            'request': request,
            'subject_template_name': self.subject_template_name,
        }

