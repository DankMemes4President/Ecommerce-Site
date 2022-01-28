from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class Vendor(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Item(models.Model):

    def __str__(self):
        # return f"{self.item_name} - {self.item_quantity} @ {self.item_cost}"
        return self.item_name

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=256)
    item_image = models.ImageField()
    item_description = models.TextField()
    item_quantity = models.PositiveIntegerField()
    item_cost = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    total_cost = models.FloatField()
    units_sold = models.PositiveIntegerField(default=0)


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    username = models.CharField(max_length=256)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    review = models.TextField()


class Customer(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    money = models.FloatField(default=0, validators=[MinValueValidator(0.0)])


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.OneToOneField(Item, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)
    total_cost = models.FloatField(default=0)


# TODO: Running into problems where if a vendor deletes an item that has already been ordered, the order disappears
# FIX: Make another class for ordered items and link it to the order with a foreign key
class Order(models.Model):

    def __str__(self):
        return self.id

    # vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    # vendor = models.ManyToManyField(Vendor)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # customer = models.ManyToManyField(Customer)
    # item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField()
    total_cost = models.FloatField(default=0)


class OrderedItems(models.Model):

    def __str__(self):
        return self.item_name

    # Since you are not allowed to order from multiple vendors for now, having a vendor link in ordered items doesn't make sense
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=256)
    item_image = models.ImageField()
    item_description = models.TextField()
    item_quantity = models.PositiveIntegerField()
    item_cost = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
    total_cost = models.FloatField()


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()


class WishList(models.Model):

    def __str__(self):
        return str(self.items)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
