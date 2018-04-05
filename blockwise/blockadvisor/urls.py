from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path('', views.index, name='index'),
    path('locations/', views.LocationListView.as_view(), name='location'),
    path('locations/<int:pk>', views.LocationDetailView.as_view(), name='location-detail'),
]
