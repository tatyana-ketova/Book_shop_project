from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.PositiveSmallIntegerField()


    def __str__(self):
        return self.user.username
        return self.user.id


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Book(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_description = models.CharField(max_length=500)
    quantity = models.IntegerField(default=False,null=False,blank=False)
    publisher = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', blank=True)
    price = models.FloatField()

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    order_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Order_details(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.order_id)


class Payment(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    book_qty = models.IntegerField(null=False,blank=False)
    created_at= models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.book_qty*self.book.price

class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
