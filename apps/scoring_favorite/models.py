from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator


class Scoring(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name="scoring_product" ,on_delete=models.CASCADE)
    scoring_user = models.ForeignKey(CustomUser, verbose_name="کاربر امتیاز دهنده",related_name="scoring_user1" ,on_delete=models.CASCADE)
    register_date = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ درج")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5) ])
    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"

    def __str__(self):
        return f"{self.product}-{self.scoring_user}"

#----------------------------------------------------

class Favorite(models.Model):
    product = models.ForeignKey(Product, verbose_name="کالا",related_name="favorite_product" ,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name="کاربر علاقه مند",related_name="favorite_user" ,on_delete=models.CASCADE)
    register_date = models.DateTimeField( auto_now_add=True, verbose_name="تاریخ درج")

    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "علاقه مندی ها"

    def __str__(self):
        return f"{self.product }{ self.user}"

 
