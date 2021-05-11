from django.urls import path
from Shop_API import views

app_name = 'Shop_API'

urlpatterns = [
    path('', views.Home.as_view(), name = 'home'),
]
