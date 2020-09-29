from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lanz/', include('lanz.urls', namespace='lanz')),
    path('account/', include('account.urls', namespace='account')),
]
