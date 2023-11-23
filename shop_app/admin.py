from django.contrib import admin
from shop_app.models import Customer, Category, Order, Order_details, Payment, Book


admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Order_details)
admin.site.register(Payment)
admin.site.register(Book)
