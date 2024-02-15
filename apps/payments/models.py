from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone


class Payment(models.Model):
    order = models.ForeignKey(Order, verbose_name="سفارش", on_delete=models.CASCADE,related_name="payment_order")
    customer = models.ForeignKey(Customer, verbose_name="مشتری", on_delete=models.CASCADE,related_name="payment_customer")
    register_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ثبت پرداخت")
    update_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش پرداخت")
    amount = models.IntegerField(verbose_name="مبلغ پرداخت")
    decription = models.TextField("توضیحات پرداخت")
    is_finally = models.BooleanField(default=False,verbose_name="وضعیت پرداخت")

    status_code = models.IntegerField(verbose_name="کد وضعیت درگاه پرداخت", null=True, blank=True)
    ref_id = models.CharField(max_length=50, verbose_name="کد پیگیری پرداخت", null=True, blank=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"

    def __str__(self):
        return f"{self.order} {self.customer} {self.ref_id}"
   
