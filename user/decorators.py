from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.shortcuts import redirect
from functools import wraps
from django.utils.decorators import available_attrs

'''
old way, rewriting django behavior that already exists

def custom_login_required(view):
    @wraps(view, assigned=available_attrs(view))
    def new_view(request, *args, **kwargs):
        user = get_user(request)
        if user.is_authenticated:
            return view(request, *args, **kwargs)
        else:
            url = "{}?next={}".format(settings.LOGIN_URL, request.path)
            return redirect(url)
    return new_view()
'''

def require_authenticated_permission(permission):
    def decorator(view):
        check_auth = (method_decorator(login_required))
        check_perm = (
            method_decorator(permission_required(permission, raise_exception=True))
        )
        decorated_view = check_auth(check_perm(view))
        return decorated_view
    return decorator


def custom_login_required(view):
    decorator = method_decorator(login_required())
    decorator_view = decorator(view)
    return decorator_view

def class_login_required(cls):
    if (not isinstance(cls, type) or not issubclass(cls, View)):
        raise ImproperlyConfigured('class_login_required should be applied to subclasses')
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    #The condition on lines 11 and 12 is trickier. In Python, everything is an object—including classes.
    # They’re objects created by the type object. To make sure that we are applying our decorator to a class,
    # we therefore ask if we’re applying the decorator to an instance of type on line 11.
    # Then, to make sure that dispatch() actually exists, we make sure
    # that the class is a subclass of View, Django’s CBV. In the event one of these is false, we raise
    # an ImproperlyConfigured exception.
    return cls

def require_authenticated_permission(permission):
    def decorator(cls):
        if (not isinstance(cls, type) or not issubclass(cls, View)):
            raise ImproperlyConfigured('require_authenticated_permission should be applied to subclasses')
        check_auth = (method_decorator(login_required))
        perm_auth = (permission_required(permission, raise_exception=True))
        cls.dispatch = (perm_auth(check_auth(cls.dispatch)))
        return cls