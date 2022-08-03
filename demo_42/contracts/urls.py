# contracts/urls.py
from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.index),
    path('contracts/', views.contracts_list, name='ice_cream_list'),
    path('contracts/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('contracts/<int:contract_id>/edit/', views.contract_edit, name='contract_edit'),
    path('create/', views.contract_new, name='contract_new'),
    path('contracts/<int:pk>/del/', views.contract_del, name='contract_del'),
]