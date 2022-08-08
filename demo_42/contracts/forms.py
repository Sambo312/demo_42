from django import forms
from django.contrib.auth import get_user_model

from .models import Partner, Contract, UserContraсts

User = get_user_model()

class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = (
            'name', 'number', 'start_date', 'end_date', 'file')
        labels = {
            'name': 'Наименование договора',
            'number': 'Номер договора',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'file': 'Файл договора',
        }


class PartnerForm(forms.ModelForm):

    class Meta:
        model = Partner
        fields = (
            'title', 'slug', 'description')
        labels = {
            'title': 'Наименование контрагента',
            'slug': 'Обозначение',
            'description': 'Описание',
        }


class UserContractsForm(forms.ModelForm):

    class Meta: 
        model = UserContraсts
        fields = (
            'collaborator',)
        labels = {
            'collaborator': 'Работник',
        }
