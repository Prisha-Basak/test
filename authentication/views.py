import django
from gfg import settings
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.shortcuts import render
from . tokens import generate_token

django.utils.encoding.force_text = force_str

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists! Please Try Some Other Username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered!")
            return redirect('home')
        
        if   len(username) > 10:
            messages.error(request,"Username should be less than 10 characters.")

        if pass1 != pass2:
            messages.error(request, "Passwoords Didn't Match!")

        if not username.isalnum():
            messages.error(request, "Username Must Be Alphanumeric.")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your Account Has Been Successfully Created! Please Check Your Email.")

        # weclome email

        subject = "Welcome to Potty Login"
        message = "Hello " + myuser.username + "! \n" + "Thank you for visiting my website!\nWe have also sent you a confirmation email. Please confirm your email address to activate your account. \n\n from \n Prisha Basak"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm Your Email @ Potty.com"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.username, 
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')

    return render(request, "authentication/signup.html")


def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, "authentication/index.html", {'username':username})

        else:
            messages.error(request, "Incorrect Credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failure.html')
 

def about(request):
    return render(request,'authentication/about.html')

def cart(request):
    return render(request,'authentication/cart.html')

def index(request):
    return render(request,'authentication/index.html')

def shop(request):
    return render(request,'authentication/shop.html')

def product(request):
    return render(request, 'authentication/product.html')
