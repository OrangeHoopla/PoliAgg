from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Landing'),
    path('house/<username>/',views.home2),
    path('house/',views.house),
    path('senate/',views.senate),
    path('senate/<username>/',views.home2),
    path('state/<state>/',views.state),
    path('state/',views.statelist),
    path('search/',views.search,name='search'),
]

