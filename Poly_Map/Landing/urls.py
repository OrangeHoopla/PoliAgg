from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Landing'),
    path('house/<username>/',views.home2),
    path('house/',views.home2),
]

