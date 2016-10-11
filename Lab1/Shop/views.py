import uuid
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from Shop.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

cart = []
filtered_producers = []
filtered_operations_systems = []
filtered_types = []
cost_from = None
cost_to = None
multimedia_val = True


def home(request):
    # Renders the home page
    global cost_from, cost_to
    assert isinstance(request, HttpRequest)
    phones = Phone.objects.all().filter(~Q(id__in=cart))
    if filtered_producers.__len__() > 0:
        phones = phones.filter(producer__id__in=filtered_producers)
    if filtered_operations_systems.__len__() > 0:
        phones = phones.filter(operation_system__id__in=filtered_operations_systems)
    if filtered_types.__len__() > 0:
        phones = phones.filter(type__id__in=filtered_types)
    if multimedia_val is True:
        phones = phones.filter(multimedia=multimedia_val)
    if cost_from is not None:
        phones = phones.filter(cost__gte=cost_from)
    else:
        cost_from = min(node.cost for node in phones)
    if cost_to is not None:
        phones = phones.filter(cost__lte=cost_to)
    else:
        cost_to = max(node.cost for node in phones)
    phones = phones.filter()
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'number_in_cart': cart.__len__(),
            'phones': phones,

            'producer': Producer.objects.all(),
            'filtered_producers': filtered_producers,

            'operation_system': OperationSystem.objects.all(),
            'filtered_operations_systems': filtered_operations_systems,
            'type': Type.objects.all(),
            'filtered_types': filtered_types,
            'cost_from': cost_from if cost_from is not None else '',
            'cost_to': cost_to if cost_to is not None else '',
            'multimedia': multimedia_val,
        },
    )


def order(request):
    # Renders the order page
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'order.html',
        {
            'year': datetime.now().year,
            'number_in_cart': cart.__len__(),
            'phones': Phone.objects.all().filter(id__in=cart)
        },
    )


@csrf_exempt
def complete(request):
    global cart, filtered_producers, filtered_operations_systems, filtered_types, cost_from, cost_to, multimedia_val
    cart = []
    filtered_producers = []
    filtered_operations_systems = []
    filtered_types = []
    cost_from = None
    cost_to = None
    multimedia_val = True
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'order.html',
        {
            'year': datetime.now().year,
            'number_in_cart': cart.__len__(),
            'phones': Phone.objects.all().filter(id__in=cart)
        },
    )


@csrf_exempt
def buy(request):
    assert isinstance(request, HttpRequest)
    phone_id = request.POST.get('phone', '')
    cart.append(phone_id)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def remove(request):
    assert isinstance(request, HttpRequest)
    phone_id = request.POST.get('phone', '')
    cart.remove(phone_id)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phones.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def producer(request):
    assert isinstance(request, HttpRequest)
    producer_id = uuid.UUID(request.POST.get('producer', ''))
    state = request.POST.get('state', '')
    if state != 'false':
        filtered_producers.append(producer_id)
    else:
        filtered_producers.remove(producer_id)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def operations_system(request):
    assert isinstance(request, HttpRequest)
    operations_system_id = uuid.UUID(request.POST.get('operations_system', ''))
    state = request.POST.get('state', '')
    if state != 'false':
        filtered_operations_systems.append(operations_system_id)
    else:
        filtered_operations_systems.remove(operations_system_id)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def type_phone(request):
    assert isinstance(request, HttpRequest)
    type_id = uuid.UUID(request.POST.get('type', ''))
    state = request.POST.get('state', '')
    if state != 'false':
        filtered_types.append(type_id)
    else:
        filtered_types.remove(type_id)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def cost(request):
    assert isinstance(request, HttpRequest)
    parameter = request.POST.get('parameter', '')
    value = request.POST.get('value', '')
    if value == '':
        value = None
    else:
        value = int(value)
    if parameter == 'from':
        global cost_from
        cost_from = value
    else:
        global cost_to
        cost_to = value
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )


@csrf_exempt
def multimedia(request):
    assert isinstance(request, HttpRequest)
    state = request.POST.get('state', '')
    global multimedia_val
    if state == '':
        multimedia_val = True
    else:
        multimedia_val = bool(value)
    return render(
        request,
        'index.html',
        {
            'year': datetime.now().year,
            'numberInCard': cart.__len__(),
            'phones': Phone.objects.all()
        },
        RequestContext(request)
    )
