from django.contrib import admin
from .models import Order, OrderDeatails, OrderState



class OrderDeatailsInline(admin.TabularInline):
    model = OrderDeatails
    extra  = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer","order_state","register_date","is_finally","discount",]
    inlines = [OrderDeatailsInline]

@admin.register(OrderState)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id","order_state_title",]
   
