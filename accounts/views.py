

from django.shortcuts import redirect, render
from django.contrib import messages,auth
from accounts.models import Account
from accounts.forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    form = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            username = email.split('@')[0]
            print(email,password)
            user = Account.objects.create_user(email=email, first_name=first_name, last_name=last_name,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            messages.success(request,'Register successful')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form':form,
    }

    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('home')

        else:
            messages.error(request,'Invalid login credintals')
            return redirect('login')

    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')