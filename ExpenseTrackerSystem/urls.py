"""
URL configuration for ExpenseTrackerSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from ExpenseTracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name="signup"),
    path('login/', views.LoginPage, name='login'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('logout/', views.LogoutView, name='logout'),
    path('save_transaction/', views.save_transaction, name='save_transaction'),
    path('filter/', views.filter_transactions, name='filter_transactions'),
]

