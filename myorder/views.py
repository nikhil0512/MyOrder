import os
import json
import xlwt
from Nikhil.settings import BASE_DIR, EMAIL_HOST_USER
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from xlrd import open_workbook
from myorder.models import Items
from myorder.serializers import ItemsSerializer
from django.core.mail import EmailMessage


def uploaddata(request):
    wb = open_workbook(BASE_DIR+'/items.xlsx')
    Items.objects.all().delete()
    print(wb.sheets()[0].nrows)
    for s in wb.sheets():
        for row in range(1, s.nrows):
            name = s.cell(row, 0).value
            unit = s.cell(row, 1).value
            obj = Items.objects.create(name=name, unit=unit)
            obj.save()
    obj = Items.objects.all().values()
    return HttpResponse(obj)


@csrf_exempt
def getItems(request):
    if request.method == 'GET':
        items_objs = Items.objects.filter(name__icontains=request.GET['term'])
        items_serializer = ItemsSerializer(items_objs, many=True)
        return JsonResponse(items_serializer.data, safe=False)


def home(request):
    items_unit_list = Items.objects.all().values_list('unit', flat=True)
    available_units = []
    for units in items_unit_list:
        for unit in units.split(','):
            if unit not in available_units:
                available_units.append(unit)
    return render(request, 'myorder.html', context={'units': available_units, 'base':BASE_DIR})


@csrf_exempt
def placeOrder(request):
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        address = request.POST['address']
        email = request.POST['email']
        item_dict = json.loads(request.POST['items-dict'].split(';')[0])
        create_exl(item_dict, phone)
        file_path = BASE_DIR+'/'+phone+'.xls'
        send_order(username, phone, address, file_path)
        #os.remove(file_path)
        return redirect('/myorder/', )


def create_exl(item_dict, phone):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    cols = ["Item", "Quantity", "Unit"]
    for i, header in enumerate(cols):
        sheet1.row(0).write(i, header)
    for row_index, item in enumerate(item_dict.values(), start=1):
        row = sheet1.row(row_index)
        for col_index, value in enumerate(item.values()):
            row.write(col_index, value)
    print(BASE_DIR+"/"+phone+".xls")
    book.save(BASE_DIR+"/"+phone+".xls")


def send_order(username, phone, address, file_path):
    subject = username + ' placed a order.'
    message = '''User - {}
mobile no - {}
Address - {}'''.format(username, phone, address)
    recepient = 'nikhilrajeevgupta@gmail.com'
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient, 'sketchcraftstudio@gmail.com'])
    email.attach_file(file_path)
    email.send()
