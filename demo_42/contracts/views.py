from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Contract, Partner

# Create your views here.
def index(request):
    template = 'contracts/index.html'
    title = 'Система оборота договоров'
    text = 'Главная страница проекта оборота договоров'
    context = {
        'title': title,
        'text': text,
    }
    
    return render(request, template, context)

def contracts_list(request):
    contracts = Contract.objects.all()
    template = 'contracts/contracts_list.html'
    title = 'Система оборота договоров'
    text = 'Список доступных договоров'
    context = {
        'title': title,
        'text': text,
        'contracts': contracts,
    }

    return render(request, template, context)

def contract_detail(request, contract_id):
    template = 'contracts/contract_detail.html'
    contract = get_object_or_404(Contract, pk=contract_id)
    context = {
        'contract': contract,
    }
    return render(request, template, context)

def contract_edit(request, pk):
    return HttpResponse('Редактирование договора')

def contract_new(request):
    template = 'contracts/contract_create.html'
    return render(request, template)

def contract_del(request, pk):
    return HttpResponse('Удаление договора')
