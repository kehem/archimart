from functools import wraps
from django.shortcuts import redirect

def async_login_required(view_func):
    """
    Async-safe login_required decorator.
    Redirects to login page if user is not authenticated.
    """
    @wraps(view_func)
    async def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # replace 'login' with your login URL name
        return await view_func(request, *args, **kwargs)
    return _wrapped_view
