from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('update-profile/', views.update_profile, name='update_profile'),
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
     path('add-animal', views.addAnimal, name='add_animal'),
     path('update-animal/<int:id>', views.updateAnimal, name='update_animal'),
     path('delete-animal/<int:id>', views.deleteAnimal, name='delete_animal'),
     path('user/<str:username>', views.userProfile, name='user_profile'),
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
     path('animal/for_adoption', views.animalsForAdoption, name='animals_for_adoption'),
     path('animal/for_daycare', views.animalsForDaycare, name='animals_for_daycare'),
     path('product/for_sale', views.productsForSale, name='products_for_sale'),
     path('animal_adoption/<int:id>/', views.animal_detail, name='animal_detail'),
     path('request_adoption/<int:id>/', views.request_adoption, name='request_adoption'),
     path('manage_adopt/', views.manage_adopt, name='manage_adopt'),
     path('update-password', views.change_password, name='change_password'),
     path('animal-info/', views.animal_info, name='animal_info'),
     path('know_before/', views.know_before, name='know_before'),
     path('know_before_cat/', views.know_before_cat, name='know_before_cat'),
     path('know_before_dog/', views.know_before_dog, name='know_before_dog'),
     path('animal_daycare/<int:id>/', views.animal_detail_2, name='animal_detail_2'),
     
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)