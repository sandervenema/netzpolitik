from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template import loader
from django.utils.translation import ugettext as _

import bcrypt
import hashlib
import time

from .models import Petition, Signature
from .forms import PetitionForm

def index(request):
    petition = get_object_or_404(Petition, pk=1)
    initial_signatures = petition.signature_set.filter(active=True,
            initial=True).order_by('name')
    active_signatures = petition.signature_set.filter(active=True,
            initial=False).order_by('-timestamp')
    form = PetitionForm()

    return render(request, 'petitions/index.html', {
        'petition': petition, 
        'signatures': active_signatures,
        'initial_signatures': initial_signatures,
        'form': form}) 

def sign(request):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, pk=1)
        initial_signatures = petition.signature_set.filter(active=True,
                initial=True).order_by('name')
        active_signatures = petition.signature_set.filter(active=True,
                initial=False).order_by('-timestamp')
        form = PetitionForm(request.POST)

        if form.is_valid():
            # Get values from form
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            affil = form.cleaned_data['affiliation']
            timestamp = time.time()
            hash_val = hashlib.sha256(' '.join([email, name, 
                affil, str(timestamp)]).encode('utf-8')).hexdigest()

            # Add values to db
            s = Signature(email=bcrypt.hashpw(email.encode(), bcrypt.gensalt()),
                    name=name, affiliation=affil, petition=petition, link=hash_val)
            s.save()

            # Generate confirmation url
            link = request.build_absolute_uri(reverse('confirm', 
                urlconf=None, args=[hash_val]))

            # Make a confirmation message
            subject = _('I am WikiLeaks: Confirm your signature')
            to_addr = [email]
            from_addr = 'no-reply@iamwikileaks.org'
            message_templ = loader.get_template('petitions/confirmation_mail.txt')
            message = message_templ.render({'link': link, 'name': name})

            # Send confirmation e-mail to sender
            send_mail(subject, message, from_addr, to_addr, fail_silently=True)

            # Display thank you message
            return render(request, 'petitions/thankyou.html')
        else:
            return render(request, 'petitions/index.html', {
                'petition': petition, 
                'signatures': active_signatures,
                'initial_signatures': initial_signatures,
                'form': form}) 
    else:
        # redirect to index
        return redirect('index')

# Confirmation
def confirm(request, link):
    # Set db sig to active
    s = get_object_or_404(Signature, link=link)
    s.active = True
    s.save()

    # Display thank you message + confirm message
    return render(request, 'petitions/confirmed.html')
