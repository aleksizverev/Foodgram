from django.shortcuts import render
from users.forms import CustomCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect


def sign_up(request):
    context = {}
    form = CustomCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')
    context['form'] = form
    return render(request, 'registration/sing_up.html', context)
