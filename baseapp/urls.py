from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PostView,AnimalDetailView,AddPostView,UpdatePostView,DeletePostView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('update-profile', views.update_profile, name='update_profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
     #path('post', views.post, name='post'),
     path('post/',PostView.as_view(),name='post'),
     path('animal/<int:pk>',AnimalDetailView.as_view(),name='animal-detail'),
     path('add_post/',AddPostView.as_view(),name='add_post'),
     path('update_post/<int:pk>',UpdatePostView.as_view(),name='update_post'),
     path('delete_post/<int:pk>',DeletePostView.as_view(),name='delete_post'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)