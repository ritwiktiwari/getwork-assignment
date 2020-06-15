from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.index, name="index"),
]
