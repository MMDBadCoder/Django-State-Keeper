from django.urls import path

from . import views

urlpatterns = [
    path('download/<int:packaging_id>/', views.download_file_view, name='admin-download-backup'),
]