from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import Signature

def validate_duplicate_email(email):
    if Signature.objects.filter(email=email).count() > 0:
        raise ValidationError("You can only submit the petition once!")



class PetitionForm(forms.Form):
    name = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': 'Your name'}), 
                           max_length=200)
    affiliation = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Your affiliation'}), 
                           max_length=200)
    email = forms.EmailField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': 'Your e-mail address'}),
                           validators=[validate_duplicate_email])


