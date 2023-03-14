from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from .forms import *

def ReaderSignUpView(request):
    if request.method != 'POST':
        form = ReaderSignUpForm()
    else:
        form = ReaderSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    context = {'form': form, 'user_type':'reader'}
    return render(request, 'registration/signup.html', context)
