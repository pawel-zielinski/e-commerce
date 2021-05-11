from django.urls import path
from Login_API import views

app_name = 'Login_API'

urlpatterns = [
    path('signup/', views.sign_up, name = 'signup'),
    path('login/', views.log_in, name = 'login'),
    path('logout/', views.log_out, name = 'logout'),
    path('profile/', views.user_profile, name = 'profile'),
]
