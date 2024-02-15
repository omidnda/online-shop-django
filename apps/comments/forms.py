from django import forms

class CommentForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_text = forms.CharField(
        label="",
        error_messages={"required":"این فیلد نمیتواند خالی باشد"},
        widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"نظر شما درباره  ی این کالا","rows":"4"})
    )