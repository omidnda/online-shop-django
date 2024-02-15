from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True, verbose_name="کد تخفیف")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    discount = models.IntegerField(verbose_name="درصد تخفیف", validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    user = models.ForeignKey(CustomUser,null=True,blank=True ,verbose_name="کاربر",on_delete=models.CASCADE, related_name="customer_coupon")

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural ="کدهای تخفیف"

    def __str__(self):
        return self.coupon_code
#---------------------------------------------------------------------
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name="عنوان سبد تخفیف")
    start_date = models.DateTimeField(verbose_name="تاریخ شروع")
    end_date = models.DateTimeField(verbose_name="تاریخ پایان")
    discount = models.IntegerField(verbose_name="درصد تخفیف", validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        verbose_name ="سبد تخفیف"
        verbose_name_plural = "سبدهای تخفیف"

    def __str__(self):
        return self.discount_title

#---------------------------------------------------------------------

class DiscountBasketDeatails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, on_delete=models.CASCADE, verbose_name="سبد تخفیف", related_name="discount_basket_deatails1")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="کالا", related_name="discount_basket_deatails2")

    class Meta:
        verbose_name = "جزییات سبد تخفیف"
       
    

   