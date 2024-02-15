from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.blog.models import Newsletter
from apps.accounts.models import CustomUser
from utils import send_email


@receiver(post_save, sender=Newsletter)
def send_newsletter(sender,instance,**kwargs):
    users = CustomUser.objects.filter(active_newssletter=True)
    if instance.is_active==True:
        for user in users:
            #send_email(instance.title,instance.text,user)
            print(100*"#")
            print(user,instance.title,instance.text )
            print(100*"#")