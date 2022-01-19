from django.contrib.auth.decorators import user_passes_test


def logout_required(function=None, logout_url='/'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator