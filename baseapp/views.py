from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.sites.shortcuts import get_current_site
# from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from AnimalWelfare import settings
from . tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
# from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import *
from django.urls import reverse_lazy
from pprint import pprint

# Create your views here.

def home(request):
    if is_admin(request.user):
        return redirect('baseapp:admin_dashboard')
    if request.user.is_authenticated:
        return redirect('baseapp:user_dashboard')
    return render(request, 'baseapp/index.html')

def signup(request):

    if request.user.is_authenticated:
        return redirect('baseapp:home')
    
    if request.method == "POST":
        print(request.POST)
        # username = request.POST['username']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        # email = request.POST['email']
        # pass1 = request.POST['pass1']
        # pass2 = request.POST['pass2']
        # contact = request.POST['contact']
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('baseapp:signup')

        #if User.objects.filter(email=email).exists():
            #messages.error(request, "Email Already Registered!!")
            #return redirect('signup')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('baseapp:signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!!")
            return redirect('baseapp:signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('baseapp:signup')

        newUser = User.objects.create_user(username=username, first_name=fname, last_name=lname, email=email, password=pass1)
        # newUser.contact = contact
        # Temporarily until Custom Auth Backend is Ready
        # newUser.is_active = True
        # newUser.is_staff = True
        # newUser.is_superuser = True
        # End
        newUser.is_active = False
        newUser.save()
        messages.success(request, "Your Account has been created succesfully!!")

        # Welcome Email
        subject = "Welcome to ANIMAL WELFARE Login!!"
        message = "Hello " + newUser.first_name + "!! \n" + "Welcome to Animal Welfare!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n-Animal Welfare Org."
        from_email = settings.EMAIL_HOST_USER
        to_list = [newUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email at " + current_site.domain
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
        # email.content_subtype = "html"
        email.fail_silently = True
        email.send()

        messages.success(request, "Please confirm your email address to activate your account.")
        return redirect('baseapp:signin')

    return render(request, 'baseapp/signup.html')

@login_required(login_url='signin')
def update_profile(request):
    user = request.user
    if request.method == "POST":
        pprint(request.POST)
        user.first_name = request.POST.get('fname', user.first_name)
        user.last_name = request.POST.get('lname', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        if 'contact' in request.POST:
            user.contact = request.POST['contact'] or user.contact
        if 'address' in request.POST:
            user.address = request.POST['address'] or user.address
        if 'bio' in request.POST:
            user.bio = request.POST['bio'] or user.bio
        user.dob = request.POST.get('dob', user.dob)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, "Profile Updated Successfully!!")
        return redirect('baseapp:user_profile', username=user.username)
    
    return render(request, 'baseapp/update_profile.html', {'user': user})

@login_required(login_url='signin')
def change_password(request):
    if request.method == "POST":
        user = request.user
        old_pass = request.POST['old_pass']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if not user.check_password(old_pass):
            messages.error(request, "Old password is incorrect.")
            return redirect('baseapp:change_password')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!!")
            return redirect('baseapp:change_password')

        user.set_password(pass1)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password Updated Successfully!!")
        return redirect('baseapp:change_password')

    return render(request, 'baseapp/change_password.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('baseapp:home')
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Successfully!!")
            return redirect('baseapp:home')
        else:
            messages.error(request, "Invalid Credentials!! Please try again.")
            return redirect('baseapp:signin')

    return render(request, "baseapp/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('baseapp:home')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        newUser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        newUser = None
    print(newUser)

    if newUser is not None and account_activation_token.check_token(newUser, token):
        newUser.is_active = True
        # user.profile.signup_confirmation = True
        newUser.save()
        login(request, newUser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('baseapp:signin')
    else:
        messages.success(request, "Account NOT Activated!!")
        return redirect('baseapp:signin')
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
    return redirect('baseapp:home')

#def post(request):
 #   return render(request,'baseapp/post.html')
# class PostView(ListView):
#     model = Post
#     template_name = 'baseapp/post.html'

# class AnimalDetailView(DetailView):
#     model = Post
#     template_name = 'baseapp/animaldetail.html'

# class AddPostView(CreateView):
#     model = Post
#     template_name = 'add_post.html'
#     fields = '__all__'

# class UpdatePostView(UpdateView):
#     model = Post
#     template_name = 'update_post.html'
#     fields = ['title','contact_info','body','picture','phone_number']

# class DeletePostView(DeleteView):
#     model = Post
#     template_name = 'delete_post.html'
#     success_url = reverse_lazy('post')

@login_required(login_url='signin')
def addAnimal(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST.get('title')
        age = request.POST.get('age')
        breed = request.POST.get('breed')
        description = request.POST.get('description')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        vaccinated = request.POST.get('vaccinated', False) == 'on'
        available_for = request.POST.get('available_for')

        animal = Animal(title=title, age=age, breed=breed, description=description, location=location, 
                         contact=contact, vaccinated=vaccinated, available_for=available_for, uploaded_by=request.user)

        if 'picture' in request.FILES:
            animal.picture = request.FILES['picture']

        if 'video' in request.FILES:
            animal.video = request.FILES['video']

        animal.save()

        messages.success(request, "Animal Added Successfully!!")
        return redirect('baseapp:upload_history', username=request.user.username)

    return render(request, 'baseapp/add_animal.html')

@login_required(login_url='signin')
def updateAnimal(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == "POST":
        animal.title = request.POST.get('title', animal.title)
        animal.age = int(request.POST.get('age', animal.age))
        animal.breed = request.POST.get('breed', animal.breed)
        animal.description = request.POST.get('description', animal.description)
        animal.location = request.POST.get('location', animal.location)
        animal.contact = request.POST.get('contact', animal.contact)
        animal.vaccinated = 'vaccinated' in request.POST and request.POST['vaccinated'] == 'on'
        animal.available_for = request.POST.get('available_for', animal.available_for)

        if 'picture' in request.FILES:
            animal.picture = request.FILES['picture']
        if 'video' in request.FILES:
            animal.video = request.FILES['video']

        animal.save()
        messages.success(request, "Animal Updated Successfully!!")
        return redirect('baseapp:upload_history', username=request.user.username)

    return render(request, 'baseapp/update_animal.html', {'animal': animal})

@login_required(login_url='signin')
def deleteAnimal(request, id):
    animal = Animal.objects.get(id=id)
    animal.delete()
    messages.success(request, "Animal Deleted Successfully!!")
    if is_admin(request.user):
        return redirect('baseapp:manage_animals')
    return redirect('baseapp:animal-list')

def animalList(request):
    animals = Animal.objects.all()
    return render(request, 'baseapp/animal_list.html', {'animals':animals})

def animalDetail(request, id):
    animal = Animal.objects.get(id=id)
    return render(request, 'baseapp/animal_detail.html', {'animal':animal})

@login_required(login_url='signin')
def userProfile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'baseapp/user_profile.html', {'user':user})

@login_required(login_url='signin')
def uploadHistory(request, username):
    user = User.objects.get(username=username)
    animals = Animal.objects.filter(uploaded_by=user)
    return render(request, 'baseapp/upload_history.html', {'animals':animals})

def is_admin(user):
    return user.is_active and (user.is_staff or user.is_superuser or user.is_admin)

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def adminDashboard(request):
    return render(request, 'baseapp/admin_dashboard.html')

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def manageAnimals(request):
    animals = Animal.objects.all()
    pending = animals.filter(approved=False)
    return render(request, 'baseapp/manage_animals.html', {'pending':pending})

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def approved_uploads(request):
    animals = Animal.objects.filter(approved=True)
    print(animals)
    return render(request, 'baseapp/approved_uploads.html', {'animals':animals})

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def approveAnimal(request, id):
    animal = Animal.objects.get(id=id)
    if request.method == "POST":
        animal.approved = True
        animal.save()
        messages.success(request, "Animal Approved Successfully!!")
        return redirect('baseapp:approved_uploads')
    return redirect('baseapp:manage_animals')

@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def manageAccessories(request):
    accessories = Accessories.objects.all()
    return render(request, 'baseapp/manage_accessories.html', {'accessories':accessories})

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def addAccessory(request):
    if request.method == "POST":
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']
        type = request.POST['type']
        color = request.POST['color']
        stock = request.POST['stock']

        accessory = Accessories(title=title, price=price, description=description, type=type, color=color, stock=stock, uploaded_by=request.user)
        if 'picture' in request.FILES:
            accessory.picture = request.FILES['picture']
        accessory.save()
        messages.success(request, "Accessory Added Successfully!!")
        return redirect('baseapp:manage_accessories')

    return render(request, 'baseapp/add_accessory.html')

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def updateAccessory(request, id):
    accessory = Accessories.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']
        type = request.POST['type']
        color = request.POST['color']

        accessory.title = title
        accessory.price = price
        accessory.description = description
        if 'picture' in request.FILES:
            accessory.picture = request.FILES['picture']
        accessory.type = type
        accessory.color = color
        accessory.save()
        messages.success(request, "Accessory Updated Successfully!!")
        return redirect('baseapp:manage_accessories')

    return render(request, 'baseapp/update_accessory.html', {'accessory':accessory})

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def deleteAccessory(request, id):
    accessory = Accessories.objects.get(id=id)
    accessory.delete()
    messages.success(request, "Accessory Deleted Successfully!!")
    return redirect('baseapp:manage_accessories')

def accessoriesList(request):
    accessories = Accessories.objects.all()
    return render(request, 'baseapp/accessories_list.html', {'accessories':accessories})

def viewProduct(request, id):
    product = Accessories.objects.get(id=id)
    return render(request, 'baseapp/view_product.html', {'product':product})

@login_required(login_url='signin')
def userDashboard(request):
    return render(request, 'baseapp/user_dashboard.html')

@login_required(login_url='signin')
def animalsForAdoption(request):
    animals = Animal.objects.filter(available_for='Adoption', approved=True)
    return render(request, 'baseapp/animals_for_adoption.html', {'animals':animals})

@login_required(login_url='signin')
def animalsForDaycare(request):
    animals = Animal.objects.filter(available_for='Daycare', approved=True)
    return render(request, 'baseapp/animal_for_daycare.html', {'animals':animals})

'''
@login_required(login_url='signin')
def productsForSale(request):
    products = Accessories.objects.all
    return render(request, 'baseapp/products_for_sale.html', {'products':products})

'''
# views.py

from django.db.models import Q


@login_required(login_url='signin')
def productsForSale(request):  # Update function name to match URL pattern
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    #products = Accessories.objects.all()
    #print(query)
    if query==None:
        products = Accessories.objects.all()
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if category:
            products = products.filter(type=category)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')
        return render(request, 'baseapp/products_for_sale.html',
                          {'products': products, 'query': query, 'sort_by': sort_by})

    else:
        multiple_q=Q(Q(title__icontains=query)|Q(description__icontains=query))
        products = Accessories.objects.filter(multiple_q)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if category:
            products = products.filter(type=category)

        if sort_by == 'price_low_to_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_to_low':
            products = products.order_by('-price')
        return render(request, 'baseapp/productsearch.html',
                          {'products': products, 'query': query, 'sort_by': sort_by})



