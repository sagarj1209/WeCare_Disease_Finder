from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('welcome/', views.welcome, name="info"),
    path('checkup/', views.checkup, name="checkup"),
    path('info/', views.info, name="info"),
    path('contact/', views.contact, name="Contact"),
    path('about/', views.about, name="About"),
    path('disease/', views.disease, name="Disease")
]