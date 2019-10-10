
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from SendgridDjangoDemo.authentication.views import activate_account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sendgriddemo/activate/<token>', activate_account, name='activate'),
    path('sendgriddemo/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]
