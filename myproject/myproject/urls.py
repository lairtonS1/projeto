"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from boards import views
from accounts import  views as accounts_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', accounts_view.signup, name="signup" ),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/',auth_views.LogoutView.as_view() ,name='logout'),
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('board/<int:board_id>/', views.board_topics, name="board_topics"),
    path("board/<int:board_id>/new/", views.new_topic, name="new_topic")
]
