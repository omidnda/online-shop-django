from django.db import models
from apps.accounts.models import Customer
from django.utils import timezone
from uuid import uuid4
from apps.products.models import Product
import utils


class PaymentType(models.Model):
    payment_title = models.CharField( max_length=50, verbose_name="نوع پرداخت")
    

    class Meta:
        verbose_name = "نوع پرداخت"
        verbose_name_plural = "انواع روش پرداحت"

    def __str__(self):
        return self.payment_title
#----------------------------------------------------
class OrderState(models.Model):
    order_state_title = models.CharField(max_length=50, verbose_name="عنوان وضعیت سفارش")
    

    class Meta:
        verbose_name = "وضعیت سفارش"
        verbose_name_plural = "انواع وضعیت سفارش"

    def __str__(self):
        return self.order_state_title

#----------------------------------------------------
class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name="مشتری", on_delete=models.CASCADE, related_name="orders")
    register_date = models.DateField(default=timezone.now, verbose_name="تاریخ سفارش")
    update_date = models.DateField(auto_now=True, verbose_name="تاریخ ویرایش سفارش")
    is_finally = models.BooleanField(default=False, verbose_name="نهایی شده")
    order_code = models.UUIDField(unique=True, default=uuid4, editable=False, verbose_name="کد منجصر به فرد سفارش")
    discount = models.IntegerField(blank=True, null=True, default=0, verbose_name="تخفیف روی فاکتور")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    payment_type = models.ForeignKey(PaymentType, default=None, on_delete=models.CASCADE, null=True, blank=True, verbose_name="نوع پرداخت", related_name="payment_types")
    order_state = models.ForeignKey(OrderState, verbose_name="وضعیت سفارش",related_name="orders_states" ,on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"

    def __str__(self):
        return f"{self.customer}\t{self.id}\{self.is_finaly}"
    
    #محاسبه مبلغ کل فاکتور برای استفاده در پرداخت انلاین
    def get_order_total_price(self):
        sum = 0
        for item in self.orders_deatails1.all():
            sum+=item.product.get_discounted_price()*item.qty
        order_final_price, tax = utils.price_by_tax(sum, self.discount)
        return int(order_final_price*10), tax
        

#--------------------------------------------------------------------  
class OrderDeatails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders_deatails1", verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders_deatails2", verbose_name="کالا")
    qty = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.IntegerField(verbose_name="قیمت کالا در فاکتور")

    
    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.price}\t{self.qty}"
