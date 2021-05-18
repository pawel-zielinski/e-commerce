from django.urls import path
from Paypent_API import views

app_name = 'Paypent_API'

urlpatterns = [
    path('checkout/', views.checkout, name = 'checkout'),
]
