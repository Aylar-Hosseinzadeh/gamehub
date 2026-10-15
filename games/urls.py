from django.urls import path

from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('add/', views.add_game, name='game_add'),
    path('<int:pk>/', views.detail, name='game_detail'),
    path('<int:pk>/add_to_library/', views.add_to_library, name='add_to_library',),
    path('<int:pk>/remove_from_library/', views.remove_from_library, name='remove_from_library',),
]