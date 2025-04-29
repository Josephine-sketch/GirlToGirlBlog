from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, Review

from django import forms
from django.forms.widgets import PasswordInput, TextInput


#LOGIN A USER
class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=TextInput())
    password= forms.CharField(widget=PasswordInput())
    
#REGISTER/CREATE A USER
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
        
#--Create a post
class CreateRecordForm(forms.ModelForm):
      class Meta:
        model= Post
        fields=['title','body','image']    
        
      def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateRecordForm, self).__init__(*args, **kwargs)
    
      def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
           instance.author = self.user
        if commit:
           instance.save()
        return instance     
   
    
#--Update a record
class UpdateRecordForm(forms.ModelForm):
      class Meta:
        model= Post
        fields=['title','body','image']     
        
#--Review a post
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }        