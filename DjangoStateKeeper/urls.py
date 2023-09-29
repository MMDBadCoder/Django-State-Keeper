from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('backup/', include('django_state_keeper.urls')),
    path('admin/', admin.site.urls),
]
