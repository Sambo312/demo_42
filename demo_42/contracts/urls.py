# contracts/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'contracts'

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('contracts/', login_required(views.contracts_list), name='contract_list'),
    path('contracts/<int:contract_id>/', login_required(views.contract_detail), name='contract_detail'),
    path('contracts/<int:contract_id>/edit/', login_required(views.contract_edit), name='contract_edit'),
    path('create/', login_required(views.contract_new), name='contract_new'),
    path('contracts/<int:contract_id>/del/', login_required(views.contract_del), name='contract_del'),
    path('contracts/<int:contract_id>/get/', login_required(views.get_contract_file), name='get_contract_file'),
    # JsonApi
    path('contracts/get_list/<int:user_id>/', login_required(views.list_curator_contracts), name='list_curator_contracts'),
    path('contracts/get_users/<int:contract_id>/', login_required(views.list_contract_users), name='list_contract_users'),
    path('contracts/get_contracts/<int:user_id>/', login_required(views.list_user_contracts), name='list_user_contracts'),
    # add/del
    path('contracts/<int:contract_id>/add_users/', login_required(views.contract_users), name='contract_users'),
    path('contracts/<int:contract_id>/del_users/', login_required(views.contract_users_del), name='contract_users_del'),
]