from django import forms
from .models import CustomUser
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from datetime import datetime
# from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
# from django.contrib.auth import get_user_model


class UserCreationForm(ModelForm):
    password1 = forms.CharField(max_length=20,label="گذرواژه" ,widget=forms.PasswordInput)
    password2 = forms.CharField(label="تکرار گذرواژه", max_length=20, widget=forms.PasswordInput)
    birth_date = forms.DateField(label="زادروز",initial=datetime.now() ,widget=forms.SelectDateWidget(years=range(1900, datetime.now().year))),
    #birth_date = DateInput = (forms.DateInput, {'class': 'datepicker'})
    class Meta:
        model = CustomUser
        fields = ["email","mobile_number","name","family","birth_date","gender",]
       

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 == pass2:
            if len(pass1) >= 8:
                if len(set(pass1).intersection([chr(x) for x in range(97,123)])) != 0 :
                    if len((set(pass1).intersection([chr(x) for x in range(65,91)]))) != 0 :
                        if len((set(pass1).intersection([chr(x) for x in range(48,58)]))) != 0 :
                            return pass1
                        else:
                            raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
                    else:
                        raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
            else:
                raise ValidationError(" رمز عبور باید حذاقل هشت کاراکتر باشد")  
        else:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست")
  
    def save(self, commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
#---------------------------------------------------------------------------------------
class UserChangeForm(ModelForm):
    password =  ReadOnlyPasswordHashField(label = "گذرواژه",help_text = "<h3> برای تغییر رمز عبور روی <a href = '../password'>لینک</a> کلیک کنید</h3>",)
 
    class Meta:
        model = CustomUser
        fields = ["email","mobile_number","password","name","family","birth_date","gender","is_admin","is_active",]

#---------------------------------------------------------------------------------------
#Sign up Form
class RegisterUserForm(ModelForm):
    password1 = forms.CharField(label="گذرواژه", max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"گذرواژه خود را وارد کنید",},))
    password2 = forms.CharField(label="تکرار گذرواژه", max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"گذرواژه خود را دوباره وارد کنید"}))
    class Meta:
        model = CustomUser
        fields = ["email",]
        widgets = {
            "email": forms.EmailInput(attrs={"class":"form-control", "placeholder":"ایمیل خود را وارد کنید"})
        }

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 == pass2:
            if len(pass1) >= 8:
                if len(set(pass1).intersection([chr(x) for x in range(97,123)])) != 0 :
                    if len((set(pass1).intersection([chr(x) for x in range(65,91)]))) != 0 :
                        if len((set(pass1).intersection([chr(x) for x in range(48,58)]))) != 0 :
                            return pass2
                        else:
                            raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
                    else:
                        raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
            else:
                raise ValidationError(" رمز عبور باید حذاقل هشت کاراکتر باشد")  
        else:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست")
              

#---------------------------------------------------------------------------------------
#verfify code
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(
        label="",
        error_messages={"required":"کد فعال سازی را وارد کنید"},
        widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"کد فعال سازی"})    
    )
#---------------------------------------------------------------------------------------
#loginForm
class LoginUserForm(forms.Form):
    email = forms.CharField(label="ایمیل",
                            error_messages={"reqired":"ایمیل خود را وارد کنید"},
                            widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"ایمیل خود را وارد کنید"}))
    password = forms.CharField(label="گذرواژه",
                               widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"رمز عبور خود را وارد کنید"}))
    
#--------------------------------------------------------------------------------------
class RememberPasswordForm(forms.Form):
    email = forms.EmailField(label="ایمیل",
                            error_messages={"reqired":"ایمیل خود را وارد کنید"},
                            widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"ایمیل خود را وارد کنید"}))
    
#--------------------------------------------------------------------------------------
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="گذرواژه", max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"گذرواژه خود را وارد کنید",},))
    password2 = forms.CharField(label="تکرار گذرواژه", max_length=128, widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"گذرواژه خود را دوباره وارد کنید"}))
    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 == pass2:
            if len(pass1) >= 8:
                if len(set(pass1).intersection([chr(x) for x in range(97,123)])) != 0 :
                    if len((set(pass1).intersection([chr(x) for x in range(65,91)]))) != 0 :
                        if len((set(pass1).intersection([chr(x) for x in range(48,58)]))) != 0 :
                            return pass2
                        else:
                            raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
                    else:
                        raise ValidationError("رمز عبور باید شامل حروف بزرگ و کوچک انگلیسی و عدد باشد")
            else:
                raise ValidationError(" رمز عبور باید حذاقل هشت کاراکتر باشد")  
        else:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست")
                      

#-----------------------------------------------------------------------
#فرم اپدیت پروفایل

class UpdateProfileForm(forms.Form):
    name = forms.CharField(label="",
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                           widget=forms.TextInput(attrs={"class":"form-control"}))
    family = forms.CharField(label="",
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                           widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="",
                            error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                            widget=forms.EmailInput(attrs={"class":"form-control", "readonly":"readonly"}))
    mobile_number = forms.CharField(label="",
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                           widget=forms.TextInput(attrs={"class":"form-control","readonly":"readonly"}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', "type":"date"}))

    adress = forms.CharField(label="",
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                           widget=forms.Textarea(attrs={"class":"form-control", "rows":"3"}))
#----------------------------------------------------------
# عضویت در خبرنامه
class SubscribeToNewsletterForm(forms.Form):
    email = forms.EmailField(label="",
                            error_messages={"required":"این فیلد نمیتواند خالی باشد"},
                            widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"آدرس ایمیل"}))