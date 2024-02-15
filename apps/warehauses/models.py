from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product

class WarehauseType(models.Model):
    ware_hause_type_title = models.CharField(max_length=50, verbose_name="نوع انبار")
    

    class Meta:
        verbose_name = "نوع انبار"
        verbose_name_plural = "انواع روش انبار"

    def __str__(self):
        return self.ware_hause_type_title
#--------------------------------------------------------------------
class Warehause(models.Model):
    warehause_type = models.ForeignKey(WarehauseType, verbose_name="انبار", on_delete=models.CASCADE, related_name="warehauses")
    user_registered = models.ForeignKey(CustomUser, verbose_name="کاربر انباردار", on_delete=models.CASCADE, related_name="warehauseuser_registered")
    product = models.ForeignKey(Product, verbose_name="کالا", on_delete=models.CASCADE, related_name="warehause_products")
    qty = models.IntegerField(verbose_name="تعداد")
    price = models.IntegerField(null=True, blank=True, verbose_name="قیمت واحد")
    register_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    class Meta:
        verbose_name = "انبار"
        verbose_name_plural = "انبارها"

    def __str__(self):
        return f"{self.warehause_type}  {self.product}"

#--------------------------------------------------------------------

   