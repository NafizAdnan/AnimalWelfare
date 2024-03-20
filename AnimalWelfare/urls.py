
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('baseapp.urls')),
    path('', include(('baseapp.urls', 'baseapp'), namespace='baseapp')),
]
