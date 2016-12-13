import uuid

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

from django.views.decorators.cache import cache_page

from Shop.forms import OrderForm
from Shop.tasks import send_mail
from Shop.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

session_filter = {}


def create_cart():
    new_cart = Cart()
    new_cart.save()
    cart_id = new_cart.id.hex

    return cart_id

@cache_page(10)
def home(request):
    # Renders the home page
    assert isinstance(request, HttpRequest)
    try:
        cart_id = request.session['cart_id']
    except KeyError:
        cart_id = create_cart()
        request.session['cart_id'] = cart_id

    if cart_id is None or Cart.objects.all().filter(id=cart_id).count() == 0:
        cart_id = create_cart()
        request.session['cart_id'] = cart_id

    if session_filter.get(cart_id) is None:
        session_filter[cart_id] = {}

    phones = Phone.objects.all().filter(
        ~Q(id__in=CartItem.objects.all().filter(cart_id=cart_id).values_list('item_id')))

    filtered_producers = session_filter[cart_id].get('producer')
    if filtered_producers:
        phones = phones.filter(producer__id__in=filtered_producers)

    filtered_operations_systems = session_filter[cart_id].get('operations_system')
    if filtered_operations_systems:
        phones = phones.filter(operation_system__id__in=filtered_operations_systems)

    filtered_types = session_filter[cart_id].get('type_phone')
    if filtered_types:
        phones = phones.filter(type__id__in=filtered_types)

    multimedia_val = session_filter[cart_id].get('multimedia')
    if multimedia_val:
        phones = phones.filter(multimedia=multimedia_val)

    cost_from = session_filter[cart_id].get('cost_from')
    if cost_from is not None:
        phones = phones.filter(cost__gte=cost_from)
    else:
        if not phones:
            cost_from = min(node.cost for node in Phone.objects.all())
        else:
            cost_from = min(node.cost for node in phones)

    cost_to = session_filter[cart_id].get('cost_to')
    if cost_to is not None:
        phones = phones.filter(cost__lte=cost_to)
    else:
        if not phones:
            cost_to = min(node.cost for node in Phone.objects.all())
        else:
            cost_to = max(node.cost for node in phones)
    phones = phones.filter()
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'number_in_cart': CartItem.objects.all().filter(cart_id=cart_id).__len__(),
            'phones': phones,

            'producers': Producer.objects.all(),
            'filtered_producers': filtered_producers,

            'operation_systems': OperationSystem.objects.all(),
            'filtered_operations_systems': filtered_operations_systems,
            'types': Type.objects.all(),
            'filtered_types': filtered_types,
            'cost_from': cost_from if cost_from is not None else '',
            'cost_to': cost_to if cost_to is not None else '',
            'multimedia': multimedia_val,
        },
    )


def order(request):
    # Renders the order page
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(pk=cart_id)
    cart_items = CartItem.objects.all().filter(cart_id=cart_id)
    return render(
        request,
        'order.html',
        {
            'year': datetime.now().year,
            'number_in_cart': cart_items.__len__(),
            'cart_items': cart_items,
            'total_price': cart.price_total,
            'form': None
        },
    )


@csrf_exempt
def complete(request):
    form = OrderForm(request.POST)

    cart_id = request.session['cart_id']
    cart = Cart.objects.get(pk=cart_id)
    cart_items = CartItem.objects.all().filter(cart_id=cart_id)
    if form.is_valid():
        o = Order(name=form.cleaned_data['name'], email=form.cleaned_data['email'],
                  phone=form.cleaned_data['phone'], address=form.cleaned_data['address'],
                  price_total=cart.price_total)
        o.save()

        for cart_item in cart_items:
            oi = OrderItem(order=o, item=Phone.objects.get(pk=cart_item.item.id), number=cart_item.number)
            oi.save()

        cart.delete()
        # send_mail.apply_async((o.name, price))
        send_mail.delay(o.name)
        return HttpResponseRedirect('/home')

    return render(
        request,
        'order.html',
        {
            'year': datetime.now().year,
            'number_in_cart': cart_items.__len__(),
            'cart_items': cart_items,
            'total_price': cart.price_total,
            'form': form
        }
    )


@csrf_exempt
def buy(request):
    assert isinstance(request, HttpRequest)

    phone_id = request.POST.get('phone_id', '')
    number = request.POST.get('number', '')
    cart_id = request.session['cart_id']
    cart = Cart.objects.get(pk=cart_id)

    print(number)
    added_price = Phone.objects.get(pk=phone_id).cost * int(number)
    cart_item = CartItem(cart_id=cart_id, item_id=phone_id, number=number, price=added_price)
    cart_item.save()

    cart.price_total += added_price
    cart.save()

    return HttpResponseRedirect('/')


@csrf_exempt
def remove(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    phone_id = request.POST.get('phone_id', '')
    print(phone_id)
    CartItem.objects.get(cart_id=cart_id, item_id=phone_id).delete()
    if CartItem.objects.all().filter(cart_id=cart_id).count() == 0:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/order')


@csrf_exempt
def producer(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    producer_id = uuid.UUID(request.POST.get('producer', ''))
    state = request.POST.get('state', '')
    if session_filter[cart_id].get('producer') is None:
        session_filter[cart_id]['producer'] = []
    if state != 'false':
        session_filter[cart_id]['producer'].append(producer_id)
    else:
        session_filter[cart_id]['producer'].remove(producer_id)
    return HttpResponseRedirect('/')


@csrf_exempt
def operation_systems(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    operations_system_id = uuid.UUID(request.POST.get('operations_system', ''))
    state = request.POST.get('state', '')
    if session_filter[cart_id].get('operations_system') is None:
        session_filter[cart_id]['operations_system'] = []
    if state != 'false':
        session_filter[cart_id]['operations_system'].append(operations_system_id)
    else:
        session_filter[cart_id]['operations_system'].remove(operations_system_id)
    return HttpResponseRedirect('/')


@csrf_exempt
def type_phone(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    type_id = uuid.UUID(request.POST.get('type', ''))
    state = request.POST.get('state', '')

    if session_filter[cart_id].get('type_phone') is None:
        session_filter[cart_id]['type_phone'] = []
    if state != 'false':
        session_filter[cart_id]['type_phone'].append(type_id)
    else:
        session_filter[cart_id]['type_phone'].remove(type_id)
    return HttpResponseRedirect('/')


@csrf_exempt
def cost(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    parameter = request.POST.get('parameter', '')
    value = request.POST.get('value', '')
    if value == '':
        value = None
    else:
        value = int(value)
    if parameter == 'from':
        session_filter[cart_id]['cost_from'] = value
    else:
        session_filter[cart_id]['cost_to'] = value
    return HttpResponseRedirect('/')


@csrf_exempt
def multimedia(request):
    assert isinstance(request, HttpRequest)
    cart_id = request.session['cart_id']
    state = request.POST.get('state', '')
    if state == '':
        session_filter[cart_id]['multimedia'] = True
    else:
        if state == 'true':
            session_filter[cart_id]['multimedia'] = True
        else:
            session_filter[cart_id]['multimedia'] = False
    return HttpResponseRedirect('/')


@csrf_exempt
def login(request):
    return render(
        request,
        'login.html',
        ''
    )