from django import forms
from .models import ProductModel
from django.core import validators


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__'

# def mendatory(value):
#     if len(value) == 0:
#         raise forms.ValidationError('Field is Mendatory')

def startwith(value):
    if value[0] != 'a':
        raise forms.ValidationError('Please Entered start with a character')

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=20,validators=[validators.MaxLengthValidator(8)],error_messages={'required':'field is Mandatory'})
    last_name = forms.CharField(max_length=20,validators=[validators.MaxLengthValidator(8)])
    email = forms.EmailField()
    OTP=forms.CharField(max_length=4)
    phone = forms.CharField(validators=[validators.MinLengthValidator(10),validators.MaxLengthValidator(10)])
    password = forms.CharField(validators=[validators.MinLengthValidator(8),validators.MaxLengthValidator(12)])
    confirm_password= forms.CharField(validators=[validators.MinLengthValidator(8),validators.MaxLengthValidator(12)])




