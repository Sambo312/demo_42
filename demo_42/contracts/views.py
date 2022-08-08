
import threading
import json

import xlsxwriter

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required

from .models import Contract, Partner, UserContraсts, User
from .utils import DateTimeEncoder
from .forms import UserContractsForm, PartnerForm, ContractForm


title = 'Система оборота договоров'

def index(request):
    template = 'contracts/index.html'
    text = 'Главная страница системы'
    context = {
        'title': title,
        'text': text,
    }
    
    return render(request, template, context)

@permission_required('contracts.view_contract', raise_exception=True)
def contracts_list(request):
    """Список договоров"""
    template = 'contracts/contracts_list.html'
    text = 'Список доступных договоров'
    user_group = request.user.groups.values_list('name', flat=True).first()
    user_id = request.user.id
    if user_group == 'admin_group':
        contracts = Contract.objects.all()
        context = {
            'title': title,
            'text': text,
            'contracts': contracts,
        }
    else:
        contract_id_lst = []
        contracts_lst = list(UserContraсts.objects.filter(collaborator_id=user_id).values(
            "deal_id",))
        for i in contracts_lst:
            for j in i.items():
                contract_id_lst.append(j[1])
        contracts = Contract.objects.filter(id__in=contract_id_lst)
        context = {
            'title': title,
            'text': text,
            'contracts': contracts,
        }
        print(contracts)

    return render(request, template, context)

@permission_required('contracts.view_contract', raise_exception=True)
def contract_detail(request, contract_id):
    """Карточка договора"""
    template = 'contracts/contract_detail.html'
    contract_id_lst = []
    user_id = request.user.id
    user_group = request.user.groups.values_list('name', flat=True).first()
    contracts_lst = list(UserContraсts.objects.filter(collaborator_id=user_id).values(
        "deal_id",))
    for i in contracts_lst:
        for j in i.items():
            contract_id_lst.append(j[1])
    if contract_id in contract_id_lst or user_group == 'admin_group':
        contract = get_object_or_404(Contract, pk=contract_id)
        context = {
            'title': title,
            'contract': contract,
            'user_group': user_group,
        }
        return render(request, template, context)
    else:
        template = 'contracts/contract_any.html'
        annotation = 'Ошибка просмотра карточки договора'
        text = 'Вы не имеете доступа к данному договору'
        context = {
            'title': title,
            'annotation' : annotation,
            'text': text,
        }
        return render(request, template, context)

@permission_required('contracts.change_contract', raise_exception=True)
def contract_edit(request, contract_id):
    """Редактирование не подвезли пока"""
    template = 'contracts/contract_any.html'
    annotation = 'Форма редактирования карточки договора'
    text = 'Здесь должна быть форма редактирования карточки договора'
    context = {
        'title': title,
        'annotation' : annotation,
        'text': text,
    }
    return render(request, template, context)

@permission_required('contracts.add_contract', raise_exception=True)
def contract_new(request):
    template = 'contracts/contract_any.html'
    annotation = 'Форма заведения карточки договора'
    text = 'Здесь должна быть форма создания карточки нового договора'
    context = {
        'title': title,
        'annotation' : annotation,
        'text': text,
    }
    return render(request, template, context)

@permission_required('contracts.delete_contract', raise_exception=True)
def contract_del(request, contract_id):
    """Удаление не подвезли пока"""
    template = 'contracts/contract_any.html'
    annotation = 'Удалять договора из системы не хорошо'
    text = 'Поэтому мы ничего не удаляем'
    context = {
        'title': title,
        'annotation' : annotation,
        'text': text,
    }
    return render(request, template, context)

@permission_required('contracts.view_contract', raise_exception=True)
def get_contract_file (request, contract_id):
    """Генератор xlsx файла из данных БД"""
    def file_write(book,  contract):
        with lock:
            sheet = book.add_worksheet("Договор")
            sheet.write('A1', 'Название', fh)
            sheet.write('B1', 'Нномер', fh)
            sheet.write('C1', 'Дата начала', fh)
            sheet.write('D1', 'Дата окончания', fh)
            sheet.write('E1', 'Контрагент', fh)
            sheet.write('F1', 'Куратор', fh)
            sheet.write('A2', contract.name, fd)
            sheet.write('B2', contract.number, fd)
            sheet.write('C2', contract.start_date, fdate)
            sheet.write('D2', contract.end_date, fdate)
            sheet.write('E2', contract.partner.title, fd)
            sheet.write('F2', contract.curator.first_name + ' ' + contract.curator.last_name, fd)

    contract = get_object_or_404(Contract, pk=contract_id)
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename=contract.xlsx'

    book = xlsxwriter.Workbook(response, {'in_memory': True})

    fh = book.add_format({'border': 1, 'valign': 'vcenter', 'align': 'center', 'text_wrap': True, 'bold': True})
    fd = book.add_format({'border': 1, 'valign': 'vcenter'})
    fdate = book.add_format({'border': 1, 'num_format':'yyyy-mm-dd'})

    lock = threading.Lock()
    threads = [threading.Thread(target=file_write, args=(book,  contract,)),]
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    book.close()

    return response

@permission_required('contracts.add_usercontraсts', raise_exception=True)
def contract_users(request, contract_id):
    """Добавление пользователя к договору"""
    template = 'contracts/contract_users.html'
    form = UserContractsForm(request.POST or None,)
    context = {
            'title': title,
            'form': form,
        }

    if request.method == 'POST':

        if form.is_valid():
            contract = form.save(commit=False)
            contract.deal_id = contract_id
            if UserContraсts.objects.filter(collaborator_id=contract.collaborator_id, deal_id=contract.deal_id).exists():
                template = 'contracts/contract_any.html'
                annotation = 'Ошибка добавления пользователя'
                text = 'Данный пользователь был добавлен ранее'
                context = {
                    'title': title,
                    'annotation' : annotation,
                    'text': text,
                }
                return render(request, template, context)
            else:
                contract.save()
            return redirect('contracts:contract_detail', contract_id=contract_id)

    return render(request, template, context)


# JsonAPI

@permission_required('contracts.view_contract', raise_exception=True)
def list_curator_contracts(request, user_id):
    """Показывает список договоров у куратора"""
    list_contracts = list(Contract.objects.filter(curator_id=user_id).values(
        "id", "name", "number", "start_date", "end_date"))

    return JsonResponse(
        list_contracts, safe=False, json_dumps_params={'ensure_ascii': False})


@permission_required('contracts.view_contract', raise_exception=True)
def list_contract_users(request, contract_id):
    """Показывает список пользователей имеющих доступ к договору"""
    contract_user_id_lst, list_users = [], []
    user_id = request.user.id
    user_group = request.user.groups.values_list('name', flat=True).first()
    contracts_lst = list(UserContraсts.objects.filter(deal_id=contract_id).values(
        "collaborator_id",))
    for i in contracts_lst:
        for j in i.items():
            contract_user_id_lst.append(j[1])
    contract_users = User.objects.filter(id__in=contract_user_id_lst)
    
    if user_group == 'admin_group' or user_id in contract_user_id_lst:
        for i in contract_users:
            context = {
            'name': str(i),
            'company' : str(get_object_or_404(Partner, pk=i.userprofile.company_id)),
            'position': str(i.userprofile.position),
            }
            list_users.append(context)
        return JsonResponse(list_users, safe=False, json_dumps_params={'ensure_ascii': False})
    
    return JsonResponse(['error'], safe=False, json_dumps_params={'ensure_ascii': False})
