import bcrypt

from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from .models import Signature


def validate_duplicate_email(email):
    # Get all hashes from the database and check whether there is a match.
    hashes = [e[0] for e in Signature.objects.values_list('email').all()]
    for stored_hash in hashes:
        if stored_hash is not None:
            stored_hash = stored_hash.encode() # encode as utf-8
            if bcrypt.hashpw(email.encode(), stored_hash) == stored_hash:
                raise ValidationError(_("You can only submit the petition once!"))


class PetitionForm(forms.Form):
    name = forms.CharField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your name')}), 
                           max_length=200)
    affiliation = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': _('Your affiliation')}), 
                           max_length=200, required=False)
    email = forms.EmailField(label='', 
                           widget=forms.TextInput(attrs={'placeholder': _('Your e-mail address')}),
                           validators=[validate_duplicate_email])


