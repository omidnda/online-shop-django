from django.db import models
from apps.products.models import Product
from apps.accounts.models import Customer
from django.core.validators import MinValueValidator, MaxValueValidator

class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name="comments_product" ,on_delete=models.CASCADE)
    user1 = models.ForeignKey(Customer, verbose_name="کاربر نظر دهنده",related_name="comments_user1" ,on_delete=models.CASCADE)
    user2 = models.ForeignKey(Customer,null=True,blank=True,verbose_name="کاربر تایید یا رد کننده نظر",related_name="comments_user2" ,on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="متن نظر")
    register_date = models.DateTimeField(verbose_name="تاریخ درج", auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    comment_parent = models.ForeignKey('Comment', verbose_name="والد نظر", on_delete=models.CASCADE,related_name="comments_child",null=True,blank=True) 
    class Meta:
        verbose_name = "نظر"
        verbose_name_plural ="نظرات"

    def __str__(self):
        return f"{self.product}-{self.user1}"

   
