from django.urls import path
from .views import *



urlpatterns = [
    path('user/', ConversationView.as_view(), name='conversations'),
    path('message/', MessageView.as_view(), name='messages'),
]
