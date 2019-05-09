from django import forms
from .models import Post, Request, FriendshipRequest
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tutor_name', 'tutor_num', 'tutor_career','class_info', 'image','category',]
        
class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields =['title',  'category',]
        
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text ='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        
        
class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    class Meta:
        model = User
        
        fields = ['username', 'password',]
        
class FriendForm(forms.ModelForm):
    class Meta:
        model = FriendshipRequest
        fields = ['accepted', 'refused']