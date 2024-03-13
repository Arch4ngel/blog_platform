from django import forms

from blog.models import Post, Payment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'is_private']

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_private'].widget = forms.CheckboxInput()


# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = '__all__'
