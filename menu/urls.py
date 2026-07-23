from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('menu/', views.menu_list_view, name='menu_list'),
    path('menu/item/<slug:slug>/', views.item_detail_view, name='item_detail'),
]
