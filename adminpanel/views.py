import os
import json
import xlwt
import random
from Nikhil.settings import BASE_DIR, EMAIL_HOST_USER
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from xlrd import open_workbook
from adminpanel.models import Items, Category
from adminpanel.serializers import ItemsSerializer
from django.core.mail import EmailMessage


def uploaddatatemp(request):
    wb = open_workbook(BASE_DIR+'/inventory list.xlsx')
    Items.objects.all().delete()
    Category.objects.all().delete()
    print(wb.sheets()[0].nrows)
    for s in wb.sheets():
        for row in range(1, s.nrows):
            category = s.cell(row, 1).value
            category_hindi = s.cell(row, 2).value
            category_obj, _ = Category.objects.get_or_create(name=category.capitalize(), hindiname=category_hindi)

            name = s.cell(row, 3).value
            name_hindi = s.cell(row, 4).value
            unit = s.cell(row, 5).value
            image_url = s.cell(row, 6).value
            sub_items = s.cell(row, 7).value
            obj = Items.objects.create(name=name, hindiname=name_hindi, unit=unit, image_url=image_url,
                                       sub_items=sub_items, category=category_obj)
            obj.save()
    obj = Items.objects.all().values()
    return HttpResponse(obj)


def uploaddata(request):
    if request.method == 'POST':
        file_path = request.POST['exl_file']
        wb = open_workbook(file_path)

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

    return render(request, 'upload_item.html')



@csrf_exempt
def getItems(request):
    if request.method == 'GET':
        items_objs = Items.objects.filter(name__icontains=request.GET['term'])
        items_serializer = ItemsSerializer(items_objs, many=True)
        return JsonResponse(items_serializer.data, safe=False)


def items_snippet(request, category_id, item_name):
    items = Items.objects.all()
    try:
        category_id = int(category_id)
    except TypeError:
        category_id = 0

    if category_id != 0 and item_name != 'all':
        items = items.filter(category_id=category_id, name__icontains=item_name)
    else:
        if category_id != 0:
            items = items.filter(category_id=category_id)
        if item_name != 'all':
            items = items.filter(name__icontains=item_name)
    result = {}
    if not items:
        random_number = random.randint(100000000, 999999999)
        item = {'id': random_number, 'name': item_name}
        result['temp_item'] = item
    else:
        result['items'] = items
    return HttpResponse(json.dumps(
      dict(html=render_to_string('item_snippet.html', result),
      )), content_type='application/json')


def home(request):
    items = Items.objects.all()
    items_unit_list = items.distinct().values_list('unit', flat=True)
    categories = Category.objects.all()
    available_units = []
    for units in items_unit_list:
        for unit in units.split('/'):
            if unit not in available_units:
                available_units.append(unit)

    return render(request, 'myorder.html',
                  context={'items': items, 'units': available_units, 'categories': categories, 'base':BASE_DIR})


@csrf_exempt
def placeOrder(request):
    if request.method == 'POST':

        try:
            username = request.POST['username']
            phone = request.POST['phone']
            address = request.POST['address']
            email = request.POST['email']
            item_dict = json.loads(request.POST['items-dict'].split(';')[0])
            create_exl(item_dict, phone)
            file_path = BASE_DIR+'/'+phone+'.xls'
            send_order(username, phone, address, file_path)
            os.remove(file_path)
            order_placed = True
        except Exception as e:
            print(e)
            order_placed = False
        return redirect('/adminpanel/', {'order_placed': order_placed})
    return redirect('/adminpanel/', {'error': 'Invalid Request.'})

def create_exl(item_dict, phone):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    cols = ["Item Name", "Quantity", "Unit"]
    for i, header in enumerate(cols):
        sheet1.row(0).write(i, header)
    for row_index, item in enumerate(item_dict.values(), start=1):
        row = sheet1.row(row_index)
        if item.get('new_item'):
            row.write(0, item['name'])
            row.write(1, '')
            row.write(2, '')
            row.write(3, item.get('comment', ''))

        else:
            row.write(0, item.get('name', ''))
            row.write(1, item.get('quantity', ''))
            row.write(2, item.get('unit', ''))
            row.write(3, item.get('comment', ''))
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
