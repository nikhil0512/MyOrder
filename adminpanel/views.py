import os
import json
import xlwt
import random

from Nikhil.settings import BASE_DIR, EMAIL_HOST_USER, LOGIN_URL
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from xlrd import open_workbook
from adminpanel.models import Items, Category, StoreItem, Store
from adminpanel.serializers import ItemsSerializer
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


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
            sub_items = s.cell(row, 8).value
            obj, _ = Items.objects.get_or_create(name=name, hindiname=name_hindi, unit=unit, image_url=image_url,
                                       sub_items=sub_items, category=category_obj)
            tags = s.cell(row, 7).value
            [obj.tags.add(tag.strip()) for tag in tags.split(',')]
            obj.tags.add(tags)

    obj = Items.objects.all().values()
    return HttpResponse(obj)


@login_required
def uploaddata(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(LOGIN_URL)

    if request.method == 'GET':
        store = request.user.store
        username = request.user.username

        wb = open_workbook(BASE_DIR+'/inventory list bharti plastic.xlsx')
        Items.objects.all().delete()
        #Category.objects.all().delete()
        print(wb.sheets()[0].nrows)
        for s in wb.sheets():
            for row in range(1, s.nrows):
                category = s.cell(row, 1).value
                category_hindi = s.cell(row, 2).value
                category_obj, _ = Category.objects.get_or_create(name=category.capitalize(), hindiname=category_hindi)
                name = s.cell(row, 3).value.capitalize()
                name_hindi = s.cell(row, 4).value
                unit = s.cell(row, 5).value
                image_url = username + "\\" + s.cell(row, 6).value
                sub_items = s.cell(row, 8).value
                obj, _ = Items.objects.get_or_create(name=name, hindiname=name_hindi, unit=unit, category=category_obj)
                obj.sub_items = sub_items
                obj.image_url = image_url
                obj.save()
                tags = s.cell(row, 7).value
                [obj.tags.add(tag.strip()) for tag in tags.split(',')]
                obj.tags.add(tags)

                try:
                    store_item_obj, _ = StoreItem.objects.get_or_create(item=obj, store=store)
                except:
                    pass

        obj = Items.objects.all().values()
        return HttpResponse(obj)
    else:
        user = request.user
        return render(request, 'admin/Upload_item.html', context={'user': user})


@csrf_exempt
def getItems(request):
    if request.method == 'GET':
        items_objs = Items.objects.filter(name__icontains=request.GET['term'])
        items_serializer = ItemsSerializer(items_objs, many=True)
        return JsonResponse(items_serializer.data, safe=False)


def items_snippet(request, slug, category_id, item_name):
    items = Items.objects.filter(id__in=Store.objects.get(slug=slug).storeitem_set.all().values_list('item', flat=True))
    try:
        category_id = int(category_id)
    except TypeError:
        category_id = 0

    if category_id != 0 and item_name != 'all':
        items = items.filter(category_id=category_id, tags__name__icontains=item_name).distinct()
    else:
        if category_id != 0:
            items = items.filter(category_id=category_id)
        if item_name != 'all':
            items = items.filter(tags__name__icontains=item_name).distinct()
    result = {}
    if not items:
        random_number = random.randint(100000000, 999999999)
        available_units = ['kg', 'gram', 'ml', 'ltr', 'no.s']
        item = {'id': random_number, 'name': item_name, 'units': available_units}
        result['temp_item'] = item
    else:
        result['items'] = items
    return HttpResponse(json.dumps(
      dict(html=render_to_string('item_snippet.html', result),
      )), content_type='application/json')


def home1(request):
    categories = Category.objects.all()
    return render(request, 'myorder.html',
                  context={'categories': categories, 'base':BASE_DIR})


def home(request, slug):
    categories = Category.objects.all()
    try:
        store = Store.objects.get(slug=slug)
    except:
        return HttpResponseBadRequest
    return render(request, 'myorder.html',
                  context={'store': store, 'categories': categories, 'base':BASE_DIR})


@csrf_exempt
def placeOrder(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            phone = request.POST['phone']
            address = request.POST['address']
            email = request.POST['email']
            item_dict = json.loads(request.POST['items-dict'].split(';')[0])
            create_exl(item_dict, username, phone, address, email)
            slug = request.POST['slug']
            trader_email = Store.objects.get(slug=slug).user.email
            file_path = BASE_DIR+"//"+phone+".xls"
            send_order(username, phone, address, file_path, trader_email)
            os.remove(file_path)
            order_placed = True
        except Exception as e:
            print(e)
            order_placed = False
        return redirect('/adminpanel/home/'+slug, {'order_placed': order_placed})
    return redirect('/adminpanel/', {'error': 'Invalid Request.'})


def create_exl(item_dict, username, phone, address, email):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("PySheet1")

    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font

    sheet1.row(0).write(0, 'Customer Name-', style=style)
    sheet1.row(0).write(1, username)
    sheet1.row(1).write(0, 'Phone-', style=style)
    sheet1.row(1).write(1, phone)
    sheet1.row(2).write(0, 'Address-', style=style)
    sheet1.row(2).write(1, address)
    sheet1.row(3).write(0, 'Email-', style=style)
    sheet1.row(3).write(1, email)
    sheet1.row(4).write(0, '')

    cols = ["Item Name", "Quantity", "Unit", "Brand"]
    for i, header in enumerate(cols):
        sheet1.row(5).write(i, header, style=style)
    for row_index, item in enumerate(item_dict.values(), start=6):
        row = sheet1.row(row_index)
        row.write(0, item.get('name', ''))
        row.write(1, item.get('quantity', ''))
        row.write(2, item.get('unit', ''))
        row.write(3, item.get('brand', '')[1::])
    print(BASE_DIR+"/"+phone+".xls")
    book.save(BASE_DIR+"/"+phone+".xls")


def send_order(username, phone, address, file_path, trader_email):
    subject = username + ' placed a order.'
    message = '''User - {}
mobile no - {}
Address - {}'''.format(username, phone, address)
    recepient = ['sketchcraftstudio@gmail.com', 'gupta.nikhil.0512@gmail.com', trader_email]
    email = EmailMessage(subject, message, EMAIL_HOST_USER, recepient)
    email.attach_file(file_path)
    email.send()

