from django.urls import path
from .views import get_process_status

urlpatterns = [
    path('/', get_process_status, name='process-status'),
]

