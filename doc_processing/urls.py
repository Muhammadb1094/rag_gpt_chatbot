from django.urls import path
from .views import *



urlpatterns = [
    path('process/', UploadPdfView.as_view(), name='index'),
]
