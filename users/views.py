from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.forms import CustomCreationForm


def sign_up(request):
    context = {}
    form = CustomCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

    context['form'] = form
    return render(request, 'registration/sing_up.html', context)
