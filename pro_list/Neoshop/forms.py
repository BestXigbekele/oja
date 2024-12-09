from django import forms
from django.forms import ModelForm
from .models import products
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProForm(ModelForm):
    class Meta:
        model = products
        fields='__all__'
        widgets={
            'category':forms.Select(attrs={
'class':'form-select','placeholder':'Carigory'
        }),
        'name':forms.TextInput(attrs={
'class':'form-control','placeholder':'name'
        })
        ,'image':forms.TextInput(attrs={
'class':'form-control',"type":'file','placeholder':'name'
        })
        ,'date_time':forms.TextInput(attrs={
'class':'form-control',"type":'datetime-local','placeholder':'name'
        })
        }

class CatForm(ModelForm):
    class Meta:
        model= products
        fields= '__all__'
        

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')