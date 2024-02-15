from django import forms
from .models import PaymentType
from datetime import date
from django.utils import timezone

choice_payment_type = ((1, "پرداخت با درگاه بانکی"), (2, "پرداخت در محل"),(3, "پی پال"))
class OrderForm(forms.Form):
    name = forms.CharField(label="نام",
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"نام"}),
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"})
    family = forms.CharField(label="نام خانوادگی",
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"نام خانوادگی"}),
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"})
    birth_date = forms.DateField(label="زادروز",initial=date.today(),
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}))
    email = forms.CharField(label="ایمیل ",
                           widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"ایمیل"}),
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"})
    mobile_number = forms.CharField(label="شماره موبایل ",
                           widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"شماره موبایل"}),)
    adress = forms.CharField(label="آدرس",
                           widget=forms.Textarea(attrs={"class": "form-control", "placeholder":"آدرس", "rows":"3"}),
                           error_messages={"required":"این فیلد نمیتواند خالی باشد"})
    description = forms.CharField(label="توضیحات",
                              widget=forms.Textarea(attrs={"class": "form-control", "placeholder":"توضیحات", "rows":"4"}),
                              required=False) 
    payment_type = forms.ChoiceField(label="",
                                     choices=[(item.pk, item) for item in PaymentType.objects.all()],
                                     widget=forms.RadioSelect)      