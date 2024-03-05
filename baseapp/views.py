from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from AnimalWelfare import settings
from . tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    return render(request, 'baseapp/index.html')

def signup(request):

    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # contact = request.POST['contact']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')

        #if User.objects.filter(email=email).exists():
            #messages.error(request, "Email Already Registered!!")
            #return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        newUser = User.objects.create_user(username, email, pass1)
        newUser.first_name = fname
        newUser.last_name = lname
        # newUser.contact = contact
        # Temporarily until Custom Auth Backend is Ready
        # newUser.is_active = True
        # newUser.is_staff = True
        # newUser.is_superuser = True
        # End
        newUser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to ANIMAL WELFARE Login!!"
        message = "Hello " + newUser.first_name + "!! \n" + "Welcome to Animal Welfare!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n-Animal Welfare Org."
        from_email = settings.EMAIL_HOST_USER
        to_list = [newUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Animal_Welfare - Django Login!!"
        message2 = render_to_string('baseapp/email_confirmation.html', {

            'name': newUser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
            'token': account_activation_token.make_token(newUser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [newUser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, 'baseapp/signup.html')

@login_required(login_url='signin')
def update_profile(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        # contact = request.POST['contact']
        email = request.POST['email']
        old_pass = request.POST['old_pass']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # user = User.objects.get(username=username)
        user = request.user


        user.username = username
        user.first_name = fname
        user.last_name = lname
        user.email = email
        # user.contact = contact
        print(old_pass, pass1, pass2)
        if old_pass and pass1 and pass2:
            print("HERE")
            if not user.check_password(old_pass):
                messages.error(request, "Old password is incorrect.")
                return redirect('update_profile')

            if pass1 != pass2:
                messages.error(request, "Passwords didn't match!!")
                return redirect('update_profile')
            user.set_password(pass1)
            messages.success(request, "Password Updated Successfully!!")
        user.save()  
        update_session_auth_hash(request, user)
        messages.success(request, "Profile Updated Successfully!!")
        return redirect('update_profile')

    return render(request, 'baseapp/update-profile.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials!! Please try again.")
            return redirect('signin')

    return render(request, "baseapp/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')



def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        newUser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        newUser = None

    if newUser is not None and account_activation_token.check_token(newUser, token):
        newUser.is_active = True
        # user.profile.signup_confirmation = True
        newUser.save()
        login(request, newUser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        messages.success(request, "Account NOT Activated!!")
        return redirect('signin')
        #return render(request, 'activation_failed.html')



def account_activate(request,newUser):


    current_site = get_current_site(request)
    email_subject = "Confirm your Email @ Animal_Welfare - Django Login!!"
    message2 = render_to_string('baseapp/email_confirmation.html', {

        'name': newUser.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
        'token': account_activation_token.make_token(newUser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [newUser.email],
    )
    email.fail_silently = True
    email.send()

    messages.success(request, "Your Account has been activated!!")
    return redirect('home')

#def post(request):
 #   return render(request,'baseapp/post.html')
class PostView(ListView):
    model = Post
    template_name = 'baseapp/post.html'

class AnimalDetailView(DetailView):
    model = Post
    template_name = 'baseapp/animaldetail.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title','contact_info','body','picture','phone_number']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('post')
    
    
    
    

    


    