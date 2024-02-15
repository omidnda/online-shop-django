from django.contrib import admin
from .models import Coupon, DiscountBasket,DiscountBasketDeatails

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=["coupon_code","start_date","end_date","discount","is_active","user"]
    ordering = ["is_active"]
    
#--------------------------------------------------------------------------------

class DiscountBasketDeatailsInline(admin.TabularInline):
    model = DiscountBasketDeatails
    extra = 3

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ["discount_title","start_date","end_date","discount","is_active"]
    ordering = ("is_active",)
    inlines = [DiscountBasketDeatailsInline]
    