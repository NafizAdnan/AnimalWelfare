
from django.contrib import admin
from django.urls import path, include
from baseapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    ## path('', include('baseapp.urls')),
    path('', include(('baseapp.urls', 'baseapp'), namespace='baseapp')),
    #path('',views.test,name="test" ),
]
