from django.shortcuts import render, redirect,HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import json
import requests
from apps.orders.models import Order,OrderState
from .models import Payment
from apps.accounts.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from apps.warehauses.models import Warehause, WarehauseType


#-------------------------------------------------------------------------------------
MERCHANT = "xxxxxxxxxxxxxxxxxxxxxxxx"
ZP_API_REQUEST = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://api.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/payments/verify/'


class ZarinpalPaymentView(LoginRequiredMixin,View):  
    def get(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            user = request.user
            payment = Payment.objects.create(
                order = order,
                customer = Customer.objects.get(user=request.user),
                amount = order.get_order_total_price(),
                description = description
            )
            payment.save()
            request.session["payment_session"] = {
                "order_id" : order.id, 
                "payment_id": payment.id
            }

            data = {
            "MerchantID": MERCHANT,
            "Amount": order.get_order_total_price(),
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
            "metadata" : {"moblie": user.mobile_number, "email":user.email}
            }
        
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            try:
                response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                return response
            
            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}
        except ObjectDoesNotExist:
            return redirect("orders:checkout_order", order_id)
    
class ZarinpalPaymentVerifyView(LoginRequiredMixin,View):
    def get(self, request):
        order_id = request.session["payment_session"]["order_id"]
        payment_id = request.session["payment_session"]["payment_id"]
        order = Order.objects.get("order_id")
        payment = Payment.objects.get("payment_id")
        t_status = request.GET.get("Status")
        t_authority= request.GET["Authority"]

        if t_status == 'OK':
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_order_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_finally = True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()

                    for orderdeatails in order.orders_deatails1.all():
                        Warehause.objects.create(
                            warehause_type = WarehauseType.objects.get(id=2),
                            user_registered = request.user,
                            product = orderdeatails.product,
                            qty = orderdeatails.qty,
                            price = orderdeatails.price
                        )

                    payment.is_finally = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect("payments:show_payment_message" ,f"پرداخت موفقیت امیز بود.کد رهگیری: {str(req.json()['data']['ref_id'])}")
                elif t_status == 101:
                    order.is_finally = True
                    order.order_state=OrderState.objects.get(id=1)
                    order.save()

                    for orderdeatails in order.orders_deatails1.all():
                        Warehause.objects.create(
                            warehause_type = WarehauseType.objects.get(id=2),
                            user_registered = request.user,
                            product = orderdeatails.product,
                            qty = orderdeatails.qty,
                            price = orderdeatails.price
                        )

                    payment.is_finally = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect("payments:show_payment_message" ,f"پرداخت قبلا انجام شده است.کد رهگیری: {str(req.json()['data']['ref_id'])}")
                else:
                    payment.status_code = t_status
                    payment.save()
                    return redirect("payments:show_payment_message" ,f"خطا در فرایند پرداخت.کد وضعیت: {str(req.json()['data']['ref_id'])}")
            else:
                e_code = req.json()["errors"]["code"]
                e_message = req.json()["errors"]["message"]
                return redirect("payments:show_payment_message" ,f" خطا در فرایند پرداخت 'Error code': {e_code}, 'Error message': {e_message}")
        else:
            return redirect("payments:show_payment_message" ," خطا در فرایند پرداخت")
       

def show_payment_message(request, message):
    return render(request,"payments_app/verify.html", {"message":message})
           