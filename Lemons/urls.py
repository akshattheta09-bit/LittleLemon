from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_page, name='reservation_page'),
    path('api/', views.reservation_api, name='reservation_api'),
]