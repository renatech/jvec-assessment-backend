from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/<int:contact_id>/', ContactView.as_view(), name='contact-detail'),
    path('user/', GetLoggedInUsername.as_view(), name='contact'),
]
