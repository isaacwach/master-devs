
  
from  django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('new/profile/',views.new_profile, name='profile'),
    path('project/', views.project, name='project'),
    path('rating/<int:pk>/',views.rating,name='rating'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT)