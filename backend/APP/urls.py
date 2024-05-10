from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from APP import views
urlpatterns = [
   path('', views.Home, name='Home'),
   path('register/', views.register, name='register'),
   path('my_login/', views.my_login, name='my_login'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('user-logout/', views.user_logout, name="user-logout"),
   path('user/', views.user, name="user"),
   path('facescan/', views.detect_face, name='facescan'),
   path('cardscan/', views.scan_card, name='cardscan'),
   path('adduser/', views.adduser, name='adduser'),
   path('deleteuser/', views.deleteuser, name='deleteuser'),
   path('insertdata/', views.insertdata, name='insertdata'),
   path('insertuser/', views.insertuser, name='insertuser'),
   path('is_card_scanner_available/', views.is_card_scanner_available, name='is_card_scanner_available'),
   path('error/', views.error, name='error'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)