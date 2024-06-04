from django.urls import path
from .views import *


app_name = 'users'

urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('sign_up/', SignUp.as_view(), name='sign_up'),
]
