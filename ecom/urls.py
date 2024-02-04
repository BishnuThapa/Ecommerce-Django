
from django.contrib import admin
from django.urls import path,include

#namespacing urls
app_name='core'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls'))
]
