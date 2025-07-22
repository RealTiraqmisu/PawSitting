from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=150, null=False)
    address = models.JSONField()

class Cart(models.Model):
    customer = models.ForeignKey("shop.Customer", on_delete=models.PROTECT)
    create_date = models.DateTimeField(null=False)
    expired_in = models.IntegerField(default=60, null=False)

class CartItem(models.Model):
    cart = models.ForeignKey("shop.Cart", on_delete=models.PROTECT)
    product = models.ForeignKey("shop.Product", on_delete=models.PROTECT)
    amount = models.IntegerField(null=False, default=1)

class Order(models.Model):
    customer = models.ForeignKey("shop.Customer", on_delete=models.PROTECT)
    order_date = models.DateField(null=False)
    remark = models.TextField(null=True)

class OrderItem(models.Model):
    order = models.ForeignKey("shop.Order", on_delete=models.PROTECT)
    product = models.ForeignKey("shop.Product", on_delete=models.PROTECT)
    amount = models.IntegerField(null=False, default=1)

class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)

# class product_categories(models.Model):
#     product_category = models.ForeignKey("shop.ProductCategory")
#     product = models.ForeignKey("shop.Product")

class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True)
    remaining_amount = models.IntegerField(null=False, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    product_category = models.ManyToManyField("shop.ProductCategory")

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateField(null=False)
    remark = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentItem(models.Model):
    payment = models.ForeignKey("shop.Payment", null=False, on_delete=models.CASCADE)
    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

class PaymentMethod(models.Model):
    payment = models.ForeignKey("shop.Payment", null=False, on_delete=models.CASCADE)
    class choi(models.TextChoices):
        QR = "QR",
        CREDIT = "CREDIT"
    method = models.CharField(max_length=10, choices=choi)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)