from django.urls import path
from . import views

#namespacing urls
app_name='core'
urlpatterns = [
    path('',views.index,name='index')
]
