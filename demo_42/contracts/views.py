
import threading
import json

import xlsxwriter

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

from .models import Contract, Partner
from .utils import DateTimeEncoder



def index(request):
    template = 'contracts/index.html'
    title = 'Система оборота договоров'
    text = 'Главная страница системы'
    context = {
        'title': title,
        'text': text,
    }
    
    return render(request, template, context)

@permission_required('contracts.view_contract', raise_exception=True)
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

@permission_required('contracts.view_contract', raise_exception=True)
def contract_detail(request, contract_id):
    template = 'contracts/contract_detail.html'
    contract = get_object_or_404(Contract, pk=contract_id)
    title = 'Система оборота договоров'
    context = {
        'title': title,
        'contract': contract,
    }
    return render(request, template, context)

@permission_required('contracts.change_contract', raise_exception=True)
def contract_edit(request, contract_id):
    return HttpResponse('Редактирование договора')

@permission_required('contracts.add_contract', raise_exception=True)
def contract_new(request):
    template = 'contracts/contract_create.html'
    return render(request, template)

@permission_required('contracts.delete_contract', raise_exception=True)
def contract_del(request, contract_id):
    return HttpResponse('Удаление договора')

@permission_required('contracts.view_contract', raise_exception=True)
def get_contract_file (request, contract_id):

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

@permission_required('contracts.view_contract', raise_exception=True)
def list_curator_contracts(request, user_id):
    list_contracts = list(Contract.objects.filter(curator_id=user_id).values(
        "id", "name", "number", "start_date", "end_date", "partner", "partner_id", "curator", "curator_id"))

    list_contracts = json.dumps(
        list_contracts, indent=4, ensure_ascii=False, cls=DateTimeEncoder)

    print (list_contracts)

    return JsonResponse(
        list_contracts, safe=False, json_dumps_params={'ensure_ascii': False})
