from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django. views import View
from .shopcart import ShopCart
from apps.products.models import Product
from .models import Order, OrderDeatails, PaymentType
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from .forms import OrderForm
import utils
from apps.discount.forms import CouponForm
from apps.discount.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
#--------------------------------------------------------------
class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        context = {"shop_cart":shop_cart}
        return render(request, "orders_app/shopcart.html", context)
    
#--------------------------------------------------------------
def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price = shop_cart.calc_total_price()
    order_final_price, tax = utils.price_by_tax(total_price) 
    context = {
        "shop_cart":shop_cart,
        "shop_cart_count":shop_cart.count,
        "total_price" : total_price,
        "tax" : tax,
        "order_final_price":order_final_price
    }
    return render(request, "orders_app/partials/show_shopcart.html", context)
#--------------------------------------------------------------
def add_to_shop_cart(request):
    product_id = request.GET.get("product_id")
    qty = request.GET.get("qty")
    product = get_object_or_404(Product, id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.add_to_shop_cart(product, qty)
    return HttpResponse(shop_cart.count)

#--------------------------------------------------------------
def delete_from_shop_cart(request):
    product_id = request.GET.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect("orders:show_shop_cart")
#--------------------------------------------------------------   
def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart=ShopCart(request)
    shop_cart.update_shop_cart(product_id_list,qty_list)
    return redirect('orders:show_shop_cart')

#--------------------------------------------------------------
#نمایش تعداد کالای موجود در سبد خرید 
def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)

#--------------------------------------------------------------
#کلاس ثبت سفارش
class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            customer =Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)

        order = Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType, id=1))

        shop_cart = ShopCart(request)
        for item in shop_cart:
            OrderDeatails.objects.create(
                order=order,
                product =item["product"],
                qty = item["qty"],
                price = item["price"],
            )
        return redirect('orders:checkout_order', order.id)
    
#--------------------------------------------------------------
#نمایش صفحه چک اوت
class CheckoutOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user = user,)
        order = get_object_or_404(Order, id=order_id)
        shop_cart= ShopCart(request)
        total_price = shop_cart.calc_total_price()
        order_final_price, tax = utils.price_by_tax(total_price, order.discount) 

        data = {
            "name":user.name,
            "family":user.family,
            "email":user.email,
            "mobile_number":user.mobile_number,
            "adress":customer.adress,
            "birth_date":user.birth_date,
            "description":order.description
        }
        form = OrderForm(data)
        coupon_form = CouponForm()
        context = {
            "shop_cart":shop_cart,
            "total_price":total_price,
            "tax":tax,
            "order_final_price":order_final_price,
            "form":form,
            "coupon_form":coupon_form,
            "order":order,
        }
        return render(request, "orders_app/checkout.html", context)
    
    def post(self, request, order_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                order = Order.objects.get(id=order_id)
                order.description = cd["description"]
                order.payment_type = PaymentType.objects.get(cd["payment_type"])
                order.save()
                
                user = request.user
                user.name = cd["name"]
                user.family = cd["family"]
                user.email = cd["email"]
                user.mobile_number = cd["mobile_number"]
                user.birth_date = cd["birth_date"]
                user.save()

                customer = Customer.objects.get(user=user)
                customer.adress = cd["adress"]
                customer.save()
                messages.success(request,"اطلاعات با موفقیت ثبت شد","success")
                return redirect("payments:zarinpal_payment",order_id)
            except:
                messages.error(request, "فاکتوری با این مشخصات یافت نشد", "danger")
                return redirect("orders:checkout_order", order_id)
        return redirect("orders:checkout_order",order_id)
        
#--------------------------------------------------------------
class ApplyCouponView(View):
    def post(self, request, *args, **kwargs):  
        order_id = kwargs["order_id"]
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            cd = coupon_form.cleaned_data
            coupon_code = cd["coupon_code"]
            coupon=Coupon.objects.filter(
                Q(coupon_code = coupon_code) &
                Q(is_active = True) &
                Q(start_date__lte=datetime.now()) &
                Q(end_date__gte=datetime.now()) &
                Q(user = request.user)
            )
            discount = 0
            try:
                order = Order.objects.get(id=order_id)
                this_coupon = Coupon.objects.get(coupon_code=coupon_code)
                if coupon:
                    discount = coupon[0].discount
                    order.discount = discount
                    order.save()
                    messages.success(request,"اعمال تخفیف با موفقیت اعمال شد","success")
                    this_coupon.is_active=False
                    this_coupon.save()
                    return redirect("orders:checkout_order", order_id)
                else:
                    order.discount = discount
                    order.save()
                    messages.error(request,"کد وارد شده معتبر نمیباشد","danger")
                    return redirect("orders:checkout_order", order_id)
            except ObjectDoesNotExist:
                messages.error(request,"سفارش موجود نیست","danger")
                return redirect("orders:checkout_order",order_id)