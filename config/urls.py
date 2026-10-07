"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from games import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('games/add/', views.add_game, name='game_add'),
    path('games/<int:pk>/', views.detail, name='game_detail' ),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name= "logout"),
    path('games/<int:pk>/add_to_library/', views.add_to_library, name= "add_to_library"),
    path('games/<int:pk>/remove_from_library/', views.remove_from_library, name= "remove_from_library")
]
