from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/' , views.upload, name='upload'),
    path('contact/', views.contactView, name="contact"),
    path("success/", views.successView, name="success"),
]
