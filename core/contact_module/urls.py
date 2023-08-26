from django.urls import path
from .views import contactus

app_name = 'contact_module'

urlpatterns = [
    path('', contactus, name='contact')
]
