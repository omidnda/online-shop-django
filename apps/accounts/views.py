from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (RegisterUserForm,VerifyRegisterForm,LoginUserForm,
                     RememberPasswordForm,ChangePasswordForm, UpdateProfileForm,
                     SubscribeToNewsletterForm)
from .models import CustomUser, Customer
import utils
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from apps.payments.models import Payment

class RegisterUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request,"accounts_app/register.html",{"form":form})
    
    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            active_code = utils.create_random_code(5)
            CustomUser.objects.create_user(
                    email=user["email"],
                    active_code=active_code,
                    password=user["password2"]
            )
            utils.send_email("کد فعال سازی", f"کد فعال سازی حساب شما {active_code} می باشد",user["email"])
            request.session["user_session"] = {
                "active_code": str(active_code),
                "email" : user["email"],

            }
            messages.success(request, "کد فعال سازی به ایمیل شما ارسال شد","success")
            return redirect("accounts:verify")
        messages.error(request, "خطا در انجام ثبت نام","danger")
        return render(request,"accounts_app/register.html",{"form":form})
#---------------------------------------------------------------------------

class VerifyRegisterCodeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm
        return render(request,"accounts_app/verify_register_code.html",{"form":form})
    
    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session["user_session"]
            if data["active_code"] == user_session["active_code"]:
                user = CustomUser.objects.get(email=user_session["email"])
                user.is_active = True
                user.active_acode = utils.create_random_code(5)
                user.save()
                messages.success(request,"به فروشگاه محصولات ارگانیک خوش آمدید", "success")
                return redirect("main:index")
            else:
                messages.error(request,"کد وارد شده اشتباه است","danger")
                return render(request,"accounts_app/verify_register_code.html",{"form":form})
        messages.error(request, "اطلاعات وارد شذه اشتباه است","danger")
        return render(request,"accounts_app/verify_register_code.html",{"form":form})
#---------------------------------------------------------------------------    

class LoginUserView(View):
    template_name = "accounts_app/login.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = LoginUserForm
        return render(request, self.template_name, {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user = authenticate(username=data["email"], password= data["password"])
            if user is not None:
                db_user = CustomUser.objects.get(email=data["email"])
                if db_user.is_admin==False:
                    messages.success(request, "خوش آمدید","success")
                    login(request, user)
                    nex_url = request.GET.get("next")
                    if nex_url is not None:
                        return redirect(nex_url)
                    else:
                        return redirect("main:index")
                else:
                    messages.error(request, "از صفحه مدیربت وارد شوید", "warning")
                    return redirect("main:index")
            messages.error(request,"اطلاعات وارد شده نادرست است", "danger")
            return render(request, self.template_name, {"form":form})
        messages.error(request,"اطلاعات وارد شذه نامعتبر است", "danger")
        return render(request, self.template_name, {"form":form})
#---------------------------------------------------------------------------

class LogoutUserView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        session_data = request.session.get("shop_cart")
        logout(request)
        request.session["shop_cart"] = session_data
        return redirect("main:index")
#--------------------------------------------------------------------------
class ChangePasswordView(View):
    template_name = "accounts_app/change_password.html"
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name,{"form":form})
        
    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(forget_password_token = kwargs["token"])
                user.set_password(data["password1"])
                token = str(uuid.uuid4())
                user.forget_password_token = token
                user.save()
                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد", "success")
                return redirect("accounts:login")
            except ObjectDoesNotExist:
                messages.error(request, "دوباره تلاش کنید", "danger")
                return redirect("accounts:remember_password")
        else:
            messages.error(request, "گذرواژه وارد شده مورد قبول نمی باشد","danger")
            return render(request, self.template_name,{"form":form})
#--------------------------------------------------------------------------
class RememberPasswordView(View):
    template_name = "accounts_app/remember_password.html"
    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request,self.template_name, {"form":form} )
    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(email = data["email"])
                if user:
                    token = str(uuid.uuid4())
                    message = f" با کلیک کردن روی پیوند زیر میتوانید گذرواژه خود را بازیابی کنید http://127.0.0.1:8000/accounts/change_password/{token}/"
                    utils.send_forget_password_mail(data["email"], token, message)
                    user.forget_password_token = token
                    user.save()
                    messages.success(request, "لینک تغییر گذرواژه به ایمیل شما ارسال شد", "success")
                    return render(request, self.template_name, {"form":form})                    
                else:
                    messages.error(request, "ایمیل وارد شده نادرست است", "danger")
                    return render(request, self.template_name, {"form":form})
            except ObjectDoesNotExist:
                messages.error(request, "اطلاعات نامعتبر است", "danger")
                return render(request, self.template_name, {"form":form})
            

#--------------------------------------------------------------------------
#پنل کاربری
class UserPanelView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user= request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "mobile_number":user.mobile_number,
                "birth_date":user.birth_date,
                "adress":customer.adress
            }

        except ObjectDoesNotExist:
            user_info = {
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "mobile_number":user.mobile_number,
                "birth_date":user.birth_date,
            }
        return render(request,"accounts_app/user_panel.html",{"user_info":user_info})

#-------------------------------------------------------------------------
@login_required
def show_last_orders(request):
    orders = Order.objects.filter(customer_id = request.user.id).order_by("-register_date")[:8]
    return render(request,"accounts_app/partials/show_last_orders.html",{"orders":orders} )

@login_required
def show_user_payments(request):
    payments = Payment.objects.filter(customer_id = request.user.id).order_by("-register_date")
    return render(request,"accounts_app/partials/show_user_payments.html",{"payments":payments} )

#--------------------------------------------------------
#ویرایش پروفایل

class UpdateProfileView(View):
    def get(self, request):
        user=request.user
        try:
            customer = Customer.objects.get(user=request.user)
            initial_dict = {
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "mobile_number":user.mobile_number,
                "birth_date":user.birth_date,
                "adress":customer.adress
            }
        except ObjectDoesNotExist:
            initial_dict={
                "name":user.name,
                "family":user.family,
                "email":user.email,
                "mobile_number":user.mobile_number,
                "birth_date":user.birth_date,
            }
        form = UpdateProfileForm(initial=initial_dict)
        return render(request,"accounts_app/update_profile.html",{"form":form} )
        
    def post(self, request):
        form = UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.name = cd["name"]
            user.family = cd["family"]
            user.email = cd["email"]
            user.mobile_number = cd["mobile_number"]
            user.birth_date = cd["birth_date"]
            user.save()
            try:
                customer = Customer.objects.get(user=request.user)
                customer.adress=cd["adress"]
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=request.user,
                    adress=cd["adress"]
                )
            messages.success(request,"اطلاعات با موفقیت ویرایش شد", "success")
            return redirect("accounts:userpanel")
        else:
            messages.error(request,"اطلاعات وارد شده معتبر نیست", "danger")
            return render(request,"accounts_app/update_profile.html",{"form":form} )
        

#----------------------------------------------------------------------
#عضویت دد خبرنامه
class SubscribeToNewsletterView(LoginRequiredMixin,View):
    def get(self, request):
        form = SubscribeToNewsletterForm()
        return render(request, "accounts_app/partials/newsletter.html",{"form":form})
    
    def post(self, request, *args, **kwargs):
        form = SubscribeToNewsletterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = CustomUser.objects.get(email = data["email"])
                if user:
                    user.active_newssletter = True
                    user.save()
                    messages.success(request, "شما با موفقیت در خبرنامه عضو شدید", "success")
                    return redirect("main:index")                    
                else:
                    messages.error(request, "ایمیل وارد شده موجود نیست", "danger")
                    return redirect("main:index") 
            except ObjectDoesNotExist:
                messages.error(request, "اطلاعات نامعتبر است", "danger")
                return  redirect("main:index") 
            