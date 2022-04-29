

from django.shortcuts import redirect, render
from django.contrib import messages,auth
from accounts.models import Account
from accounts.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            
            user = Account.objects.create_user(email=email, first_name=first_name, last_name=last_name,username=username,password=password)
            user.phone_number=phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject =  'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Register successful, we have sent verification email ')
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
       
        user = auth.authenticate(email=email, password=password)

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

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'congratulation your account is activated.')

        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request): 
    return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject =  'reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Password  reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request,'Accoucnt does not exists')
            
    return render(request, 'accounts/forgotPassword.html')

def resetpassword(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        return redirect('resetpass')
    else:
        messages.error(request,'This link has been expired')

    return redirect('login')

def resetpass(request):
    if request.method == 'POST':
        password = request.POST['password']
        c_password = request.POST['confirm_password']

        if password == c_password:
            uid=request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            
            messages.success(request,'Your password has been reset')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            
    return render(request,'accounts/resetpass.html')