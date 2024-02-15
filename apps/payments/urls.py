from django.urls import path,include
from . import views

app_name = "payments"
urlpatterns = [
     path("zarinpal_payment/<int:order_id>/", views.ZarinpalPaymentView.as_view(), name="zarinpal_payment"),
     path("verify/<int:order_id>/", views.ZarinpalPaymentVerifyView.as_view(), name="verify"),
     path("show_payment_message/<str:message>/", views.show_payment_message,name="show_payment_message"),
    
]
