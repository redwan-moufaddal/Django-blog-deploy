from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import CustomUser

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name','placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','id': 'last_name', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Enter Your Email Address Here..'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'city','placeholder': 'Enter your city'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'country','placeholder': 'Enter your country'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'Enter your password'}), required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirm your password'}), required=True)
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','city','country','email', 'password1', 'password2')



class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'cols': 45, 
                'rows': 5, 
                'maxlength': 65525, 
                'required': 'required',
                'class': 'comment-form-comment'
            }
        ),
        label='Comment'
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'required': 'required',
                'class': 'comment-form-author'
            }
        ),
        label='Name',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'required': 'required',
                'class': 'comment-form-email'
            }
        ),
        label='Email'
    )


