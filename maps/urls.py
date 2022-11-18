from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('map/', views.map, name="map"),
    path('map/<str:x>/<str:y>/', views.map_search, name="map_search"),
    path('map/search/<str:x>/<str:y>/', views.search, name="search"),
]