# Create your views here.
import jwt
from django.shortcuts import redirect, render

from SendgridDjangoDemo.authentication.models import User
from SendgridDjangoDemo.settings import SECRET_KEY, DOMAIN


def activate_account(request, token):
    username = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])["user"]
    user = User.objects.get(username=username)
    if username and not user.is_verified:
        user.is_verified = True
        user.save()
        return redirect(f'{DOMAIN}/sendgriddemo/')
