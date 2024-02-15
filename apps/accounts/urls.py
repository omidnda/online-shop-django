from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("verify/", views.VerifyRegisterCodeView.as_view(), name="verify"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.LogoutUserView.as_view(), name="logout"),
    path("userpanel/", views.UserPanelView.as_view(), name="userpanel"),
    path("show_last_orders/", views.show_last_orders, name="show_last_orders"),   
    path("show_user_payments/", views.show_user_payments, name="show_user_payments"),   
    path("remember_password/", views.RememberPasswordView.as_view(), name="remember_password"),
    path("change_password/<token>/", views.ChangePasswordView.as_view(), name="change_password"),
    path("update_profile/", views.UpdateProfileView.as_view(), name="update_profile"),    
    path("newsletter/", views.SubscribeToNewsletterView.as_view(), name="newsletter"),  
]
