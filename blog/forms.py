from django import forms

from blog.models import Post, Payment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'is_private']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget = forms.Select
