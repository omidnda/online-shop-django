from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone



class CustomUserManager(BaseUserManager): 
    def create_user(self, email, mobile_number="", name="", family="",active_code=None,password=None,gender=None,birth_date=None):
        if not email:
            raise ValueError("وارد کردن ایمیل الزامی است")
        user= self.model(
            email = self.normalize_email(email),
            mobile_number=mobile_number,
            name=name,
            family=family,
            active_code = active_code,
            gender=gender,
            birth_date=birth_date
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,email,mobile_number, name, family,password=None,active_code=None, gender=None,birth_date=None):
        user=self.create_user(
            email=email,
            mobile_number=mobile_number,
            name=name,
            family=family,
            active_code = active_code,
            gender=gender,
            birth_date=birth_date,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

# =====================================================================

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True, max_length=200,verbose_name="ایمیل")
    mobile_number = models.CharField(max_length=15, blank=True,verbose_name="شماره موبایل")
    name = models.CharField(max_length=20,blank=True,verbose_name="نام")
    family = models.CharField(max_length=20,blank=True,verbose_name="نام خانوادگی")
    birth_date = models.DateField(blank=True,null=True,verbose_name="زادروز")
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    register_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ ثبت")
    GENDER_CHOICES = (("1", "مرد"), ("2","زن"),("3", "دیگر"))
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES, default="1", blank=True, null=True,verbose_name="جنسیت")
    is_active = models.BooleanField(default=False,verbose_name="فعال /غیرفعال")
    active_code = models.CharField(max_length=100, null=True, blank=True,verbose_name="کد فعال سازی")
    is_admin = models.BooleanField(default=False,verbose_name="مدیر سایت")
    active_newssletter = models.BooleanField(default=False,verbose_name="ارسال خبرنامه")
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile_number", "name", "family"]
    objects = CustomUserManager()
    def __str__(self) -> str:
        return  f"{self.name} {self.family}"

    @property
    def is_staff(self):
        return self.is_admin
      
# =====================================================================
class Customer(models.Model):
    user= models.OneToOneField(CustomUser, verbose_name="مشتری", on_delete=models.CASCADE, primary_key=True)
    adress = models.TextField(null=True, blank=True)
   
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتری ها"

    def __str__(self):
        return self.user.name 

    