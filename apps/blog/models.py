from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Newsletter(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    text = RichTextUploadingField()
    is_active = models.BooleanField(default=False, verbose_name="وضعیت")
    

    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه ها"

    def __str__(self):
        return self.title
