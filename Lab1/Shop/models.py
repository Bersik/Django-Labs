import uuid
from django.db import models


class Producer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class OperationSystem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Phone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    operation_system = models.ForeignKey(OperationSystem, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    multimedia = models.BooleanField()
    cost = models.IntegerField()

    image = models.CharField(max_length=250)

    description = models.CharField(max_length=1000, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    price_total = models.IntegerField(default=0)


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Phone, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    price = models.IntegerField(default=0)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    price_total = models.DecimalField(default=0, max_digits=1000, decimal_places=2)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Phone, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def __unicode__(self):
        return self.item.name
