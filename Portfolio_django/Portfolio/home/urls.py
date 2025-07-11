from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("", views.index,name='home'),
    path("aboutme", views.aboutme,name='aboutme'),
    path("service",views.service,name="service"),
]