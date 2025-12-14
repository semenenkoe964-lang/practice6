from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_pokemon, name='search'),
    path('add/', views.add_pokemon, name='add_pokemon'),
    path('remove/<int:pokemon_id>/', views.remove_pokemon, name='remove_pokemon'),
    path('detail/<int:pokemon_id>/', views.detail_pokemon, name='detail_pokemon'),
    path('battle/', views.battle, name='battle'),
]