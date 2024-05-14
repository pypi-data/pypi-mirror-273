# django-email-auth
A simple Django app to authenticate users via email (or username).

## Installation

1. Add the package to the project in the usual way according to your project toolset (pip, poetry, pyenv, uv, etc.).
2. Add the following to your `INSTALLED_APPS` setting:
```python
INSTALLED_APPS = [
    ...
    'email_auth',
    ...
]
```
3. Add the `AUTHENTICATION_BACKENDS` setting:
```python
AUTHENTICATION_BACKENDS = [
    'django_email_auth.backend.EmailAuthBackend',
]
```

You can now use either your email OR username to log in.
