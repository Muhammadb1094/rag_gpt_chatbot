from django.urls import path
from .views import SignUpView, SignInView, CurrentUserView





urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
]
