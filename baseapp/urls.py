from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import PostView,AnimalDetailView,AddPostView,UpdatePostView,DeletePostView
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
     # path('post/',PostView.as_view(),name='post'),
     # path('animal/<int:pk>',AnimalDetailView.as_view(),name='animal-detail'),
     # path('add_post/',AddPostView.as_view(),name='add_post'),
     # path('update_post/<int:pk>',UpdatePostView.as_view(),name='update_post'),
     # path('delete_post/<int:pk>',DeletePostView.as_view(),name='delete_post'),
     path('add-animal', views.addAnimal, name='add_animal'),
     path('update-animal/<int:id>', views.updateAnimal, name='update_animal'),
     path('delete-animal/<int:id>', views.deleteAnimal, name='delete_animal'),
     path('animal/<int:id>', views.animalDetail, name='animal_detail'),
     path('user/<str:username>', views.userProfile, name='user_profile'),
     # path('animal', views.animal, name='animal'),
     # path('search', views.search, name='search'),
     path('user/<str:username>/upload-history', views.uploadHistory, name='upload_history'),
     path('admin-dashboard', views.adminDashboard, name='admin_dashboard'),
     path('user-dashboard', views.userDashboard, name='user_dashboard'),
     path('manage_animals', views.manageAnimals, name='manage_animals'),
     path('approve_upload/<int:id>', views.approveAnimal, name='approve_upload'),
     path('approved_uploads', views.approved_uploads, name='approved_uploads'),
     path('manage_accessories', views.manageAccessories, name='manage_accessories'),
     path('add_accessory', views.addAccessory, name='add_accessory'),
     path('update_accessory/<int:id>', views.updateAccessory, name='update_accessory'),
     path('delete_accessory/<int:id>', views.deleteAccessory, name='delete_accessory'),
     path('product/<int:id>', views.viewProduct, name='view_product'),
     # path('animal/<int:id>', views.animalDetail, name='animal_detail'),
     path('animal/for_adoption', views.animalsForAdoption, name='animals_for_adoption'),
     path('animal/for_daycare', views.animalsForDaycare, name='animals_for_daycare'),
     path('product/for_sale', views.productsForSale, name='products_for_sale'),
     path('supports',views.supports,name='supports'),
     path('supports/<slug:slug>',views.support,name='support'),
     path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
     path('request-adoption/<int:pk>/', views.request_adoption, name='request_adoption'),
     path('manage_adopt/', views.manage_adopt, name='manage_adopt'),
     path('approve_adopt/<int:pk>/', views.approve_adopt, name='approve_adopt'),
     #path('user/<int:pk>/upload-history', views.adoptionHistory, name='adoption_history'),



     ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)