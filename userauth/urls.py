from django.urls import path
from . import views

app_name='userauth'
urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up')
]