from django.db import models
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum, Avg
from middlewares.middlewares import RequestMiddleWare

#----------------------------------------------------------

class Brand(models.Model):
    upload_file = FileUpload("images", "brand")
    brand_name = models.CharField(max_length=50, verbose_name="نام برند")
    brand_logo_image = models.ImageField(upload_to=upload_file.upload_to, null=True, blank=True,verbose_name="تصویر برند کالا")
    slug = models.SlugField(max_length=200, null=True)
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def __str__(self):
        return self.brand_name
#----------------------------------------------------------
class ProductGroup(models.Model):
    upload_file = FileUpload("images", "product_group")
    group_name = models.CharField(max_length=50, verbose_name="گروه کالا")
    image_name = models.ImageField(upload_to=upload_file.upload_to, verbose_name="تصویر گروه کالا")
    description =models.TextField()
    group_parent = models.ForeignKey("ProductGroup", verbose_name="والد گروه کالا"
                                    ,blank=True,null=True, on_delete=models.CASCADE,
                                    related_name="groups")
    slug = models.SlugField(max_length=200, null=True)
    register_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ درج")
    update_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ به روز رسانی")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    

    class Meta:
        verbose_name = "گروه کالا"
        verbose_name_plural = "گروه های کالا"

    def __str__(self):
        return self.group_name

    
#----------------------------------------------------------
class Product(models.Model):
    upload_file = FileUpload("images", "products")
    product_name = models.CharField(max_length=50, verbose_name="نام کالا")
    short_description = models.TextField(null=True, blank=True)
    description =  RichTextUploadingField(null=True, blank=True)
    product_image = models.ImageField(upload_to=upload_file.upload_to,verbose_name="تصویر کالا")
    price = models.IntegerField(default=0, verbose_name="قیمت")
    slug = models.SlugField(max_length=200, null=True)
    register_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ درج")
    update_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ به روز رسانی")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    product_group = models.ManyToManyField(ProductGroup ,verbose_name="گروه کالا", related_name="products_of_groups")
    product_brand = models.ForeignKey(Brand, verbose_name="برند کالا",null=True, blank=True,related_name="product_of_brands",on_delete=models.CASCADE)
    class Meta:
        verbose_name = "کالا"
        verbose_name_plural = "کالاها"

    def get_absolute_url(self):
        return reverse("products:product_deatails", kwargs={"slug": self.slug})
    
    def get_discounted_price(self):
        discounts_list = []
        for discount_basket_deatail in self.discount_basket_deatails2.all():
            if (discount_basket_deatail.discount_basket.is_active == True and
                discount_basket_deatail.discount_basket.start_date <= datetime.now() and
                datetime.now() <= discount_basket_deatail.discount_basket.end_date):
                discounts_list.append(discount_basket_deatail.discount_basket.discount)
        discount = 0
        if len(discounts_list) > 0:
            discount = max(discounts_list)
        return self.price - (self.price*discount/100)

    #موجودی انبار
    def get_number_in_warehause(self):
        sum1 = self.warehause_products.filter(warehause_type_id = 1).aggregate(Sum("qty"))
        sum2 = self.warehause_products.filter(warehause_type_id = 2).aggregate(Sum("qty"))
        input = 0
        if sum1["qty__sum"]!=None:
            input = sum1["qty__sum"]
        output=0
        if sum2["qty__sum"]!=None:
            output = sum1["qty__sum"]
        return input-output
    
    #امتیازی که کاربر به محصول داده است
    def get_user_score(self):
        request = RequestMiddleWare(get_response=None)
        request = request.thread_local.current_request
        score=0
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count() > 0:
            score = user_score[0].score
        return score
    
    #میانگین امتیاز کالا
    def get_score_average(self):
        avgScore = self.scoring_product.all().aggregate(Avg("score"))["score__avg"]
        if avgScore == None:
            avgScore=0
        return int(avgScore)
    
    #تابع علاقه مندی ها
    def get_user_favorite(self):
        request = RequestMiddleWare(get_response=None)
        request = request.thread_local.current_request
        flag = self.favorite_product.filter(user=request.user).exists()
        return flag
    #تابع گروه اصلی کالا برای استفاده در مقایسه کالاها
    def getMainProductGroups(self):
        return self.product_group.all()[0].id

    def __str__(self):
        return self.product_name
    
#----------------------------------------------------------
class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name="نام کالا", on_delete=models.CASCADE, related_name="gallery_images")
    upload_file = FileUpload("images", "product_gallery")
    image_name = models.ImageField(upload_to=upload_file.upload_to,verbose_name="تصویر کالا")

    class Meta:
        verbose_name = "گالری تصاویر محصول"
        verbose_name_plural = "گالری تصاویر محصول"
#----------------------------------------------------------

class Feature(models.Model):
    feature_name = models.CharField( max_length=50, verbose_name="نام ویژگی")
    product_group = models.ManyToManyField(ProductGroup, verbose_name="گروه کالا",related_name="features_of_product_group")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت")
    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"

    def __str__(self) -> str:
        return self.feature_name
#----------------------------------------------------------
class FeatureValue(models.Model):
    value_title = models.CharField( max_length=50, verbose_name="مقدار")
    feature = models.ForeignKey(Feature, verbose_name="ویژگی",blank=True, null=True, on_delete=models.CASCADE,related_name="feature_values")
    
    def __str__(self) -> str:
        return str(self.id) + " " + self.value_title
    
    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی ها"

    
#----------------------------------------------------------
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, verbose_name="نام کالا", on_delete=models.CASCADE, related_name="features_of_product")
    feature = models.ForeignKey(Feature, verbose_name="ویژگی", on_delete=models.CASCADE)
    feature_value = models.CharField(max_length=50, verbose_name="مقدار ویژگی")
    filter_value = models.ForeignKey(FeatureValue, verbose_name="مقدار استاندارد", on_delete=models.CASCADE,blank=True, null=True,)
    is_active = models.BooleanField(default=True, verbose_name="وضعیت")
    class Meta:
        verbose_name = "ویژگی کالا"
        verbose_name_plural = "ویژگی های کالاها"

    def __str__(self):
        return f"{self.product} : {self.feature} : {self.feature_value}"

 