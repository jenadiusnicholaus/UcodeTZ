from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from validate_email import validate_email
from verify_email import verify_email
from django.views.generic.base import View
from .forms import UserForm, LoginForm
from .models import User
from .tokens import account_activation_token


# @login_required(login_url='login')
def dashboard(request):
    return render(request, template_name='dashboard.html')


def activate(request, uidb64, token, ):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # <-- addition
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Welcome to wewize.com, login now')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


class Register(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, template_name='authentication/register.html', context=context)

    def post(self, request, *args, **kwargs):
        form = UserForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get("password2")

            if not validate_email(email):
                messages.error(request, 'Invalid email address')
                return redirect('register')

            if password1 != password2:
                messages.warning(request, 'Password doesnt much')
                return redirect('register')

                # we need to check if the username and email address exists in dabase
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                # we meed noe to create  a user
                User.objects.create_user(email, password1, username=username, is_active=False)
                user = User.objects.get(username=username, email=email)

                # prepare to send an email address
                current_site = get_current_site(request)
                mail_subject = "activate your account now"
                message = render_to_string('authentication/account_activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)

                })
                to_email = user.email
                email_to_send = EmailMessage(
                    mail_subject,
                    message,
                    to=[to_email]
                )
                email_to_send.send()
                messages.info(self.request, f'activate your account at ****{email[3:]}')
                return redirect('login')
            else:
                messages.info(self.request, f'Username {username} and email{email} does not match')
                return redirect('register')

        print(form.data)
        messages.warning(request, 'Try to feel all fields')
        return redirect('register')


class Login(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, template_name='authentication/login.html', context=context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user_auth = authenticate(email=email, password=password)
            if not validate_email(email):
                messages.warning(self.request, 'Enter valid email')
                return redirect('login')
            if user_auth:
                # we need to check if the auth_user is activate to our system
                if user_auth.is_active:
                    # if not request.POST.get('remember_me', None):
                    # make the session to end in one mouth

                    login(request, user_auth)
                    messages.success(self.request, 'welcome home ')
                    return redirect('dashboard')

                else:
                    messages.warning(self.request, 'Your account was inactive.Try to activate your account now')
                    return redirect('login')
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(email, password))
                messages.warning(self.request, 'Invalid login details given,')
                return redirect("login")
        else:
            print(form.data)
            messages.error(self.request, 'Enter you username and password to continual')
            return redirect('login')


def logoutView(request):
    logout(request)
    messages.warning(request, 'you signed out, welcom again')
    return redirect('login')
