import random
from django.core.mail import send_mail
from django.conf import settings
from uuid import uuid4
import os

class FileUpload():
    def __init__(self, dir, prefix):
        self.dir = dir
        self.prefix = prefix
    def upload_to(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"
#------------------------------------------------------------

def create_random_code(count):
    return random.randint(10**(count-1), 10**count-1)

#------------------------------------------------------------

def send_email(subject, message, to):
    # sender = settings.EMAIL_HOST_USER
    # return send_mail(subject, message, sender, to)
    pass

#------------------------------------------------------------
def send_forget_password_mail(user, token, message): 
    # subject = "لینک بازیابی گذرواژه"
    # message = f" با کلیک کردن روی پیوند زیر میتوانید گذرواژه خود را بازیابی کنید http://127.0.0.1:8000/accounts/remember_password/{token}/"
    # sender = settings.EMAIL_HOST_USER
    # recipient_list = [user]
    # return send_mail(subject, message, sender, recipient_list)
    pass

#--------------------------------------------------------------

def price_by_tax(price, discount=0):
    tax = 0.09*(price)
    sum = price + tax
    sum =  sum-(sum*discount/100)
    return int(sum), int(tax)