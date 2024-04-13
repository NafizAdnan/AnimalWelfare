import stripe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from AnimalWelfare import settings
from . tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import *
from django.urls import reverse_lazy
from pprint import pprint
from django.urls import reverse
from .utils import *
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
    if is_admin(request.user):
        return redirect('baseapp:admin_dashboard')
    if request.user.is_authenticated:
        return redirect('baseapp:user_dashboard')
    return render(request, 'baseapp/index.html',{'room_name':"broadcast"})

# @require_POST
# def mark_notifications_read(request):
#     if request.user.is_authenticated:
#         BroadcastNotification.objects.filter(user=request.user, read=False).update(read=True)
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False}, status=401)

def signup(request):

    if request.user.is_authenticated:
        return redirect('baseapp:home')
    
    if request.method == "POST":
        print(request.POST)
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
        newUser.is_active = True
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
        
        user.contact = request.POST['contact'] or user.contact
        user.address = request.POST['address'] or user.address
        user.bio = request.POST['bio'] or user.bio
        user.dob = request.POST.get('dob') or user.dob
        user.profile_picture = request.FILES.get('profile_picture', user.profile_picture)
        remove_picture = request.POST.get('remove_picture') == 'on'
        if remove_picture:
            # user.profile_picture = None
            # user.profile_picture.delete(save=True)
            user.profile_picture.delete()
        
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
                         contact=contact, vaccinated=vaccinated, available_for=available_for, user=request.user)

        picture = request.FILES.get('picture', None)
        if picture:
            os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)
            temp_path = os.path.join(settings.TEMP_UPLOAD_DIR, picture.name)
            if is_animal_in_image(picture, temp_path):
                animal.picture = picture
                os.remove(temp_path)
            else:
                os.remove(temp_path)
                messages.error(request, "Invalid Image!!")
                return redirect('baseapp:add_animal')

        animal.video = request.FILES.get('video') if 'video' in request.FILES else None

        animal.save()

        messages.success(request, "Animal Added Successfully!!")
        return redirect('baseapp:upload_history', username=request.user.username)

    return render(request, 'baseapp/add_animal.html')

def is_animal_in_image(picture, path):

    with open(path, 'wb+') as destination:
        for chunk in picture.chunks():
            destination.write(chunk)

    upload_response = upload_image_to_imagga(path)
    print(upload_response)
    if 'upload_id' in upload_response['result']:
        upload_id = upload_response['result']['upload_id']
        categories_response = get_image_categories(upload_id)
        print(categories_response)
        if categories_response['status']['type'] == 'success':
            categories = categories_response['result']['categories']
            print(categories)
            for category in categories:
                name = category['name']
                for key in name:
                    if 'animal' in name[key].lower():
                        return True
        else:
            print("Error in getting categories!!")

    return False


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

        picture = request.FILES.get('picture')
        if picture != animal.picture:
            os.makedirs(settings.TEMP_UPLOAD_DIR, exist_ok=True)
            temp_path = os.path.join(settings.TEMP_UPLOAD_DIR, picture.name)
            if is_animal_in_image(picture, temp_path):
                animal.picture = picture
                os.remove(temp_path)
            else:
                os.remove(temp_path)
                messages.error(request, "Invalid Image!!")
                return redirect('baseapp:update_animal', id=id)

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
    return redirect('baseapp:upload_history', username=request.user.username)

def animalList(request):
    animals = Animal.objects.all()
    return render(request, 'baseapp/animal_list.html', {'animals':animals})


@login_required(login_url='signin')
def userProfile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'baseapp/user_profile.html', {'user':user})

@login_required(login_url='signin')
def uploadHistory(request, username):
    user = User.objects.get(username=username)
    animals = Animal.objects.filter(user=user)
    return render(request, 'baseapp/upload_history.html', {'animals':animals})

def is_admin(user):
    return user.is_active and (user.is_staff or user.is_superuser or user.is_admin)

@login_required(login_url='signin')
@user_passes_test(is_admin, login_url='signin', redirect_field_name=None)
def adminDashboard(request):
    return render(request, 'baseapp/admin_dashboard.html',{'room_name':"broadcast"})

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
        print(request.POST)
        title = request.POST['title']
        price = request.POST['price']
        description = request.POST['description']
        type = request.POST['type']
        color = request.POST['color']
        stock = request.POST['stock']
        accessory.title = title
        accessory.price = price
        accessory.description = description
        if 'picture' in request.FILES:
            accessory.picture = request.FILES['picture']
        accessory.type = type
        accessory.color = color
        accessory.stock = stock
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
    return render(request, 'baseapp/user_dashboard.html',{'room_name':"broadcast"})

@login_required(login_url='signin')
def animalsForAdoption(request):
    animals = Animal.objects.filter(available_for='Adoption', approved=True)
    return render(request, 'baseapp/animals_for_adoption.html', {'animals':animals})

@login_required(login_url='signin')
def animalsForDaycare(request):
    animals = Animal.objects.filter(available_for='Daycare', approved=True)
    return render(request, 'baseapp/animal_for_daycare.html', {'animals':animals})

@login_required(login_url='signin')
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        message_body = request.POST.get('message_body', '')
        if title and message_body:
            ticket = Ticket(title=title, user=request.user)
            ticket.save()
            Message.objects.create(ticket=ticket, user=request.user, body=message_body)
            messages.success(request, "Ticket Created!!")
            return redirect('baseapp:ticket_detail', ticket_id=ticket.id)

    return render(request, 'baseapp/create_ticket.html')

@login_required(login_url='signin')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    messages = ticket.messages.all()
    return render(request, 'baseapp/ticket_detail.html', {'ticket': ticket, 'inbox': messages})

@login_required(login_url='signin')
def add_message(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        body = request.POST.get('body', '')
        if body:
            Message.objects.create(ticket=ticket, user=request.user, body=body)
            return redirect('baseapp:ticket_detail', ticket_id=ticket.id)
    return render(request, 'baseapp/ticket_detail.html', {'ticket': ticket})

@login_required(login_url='signin')
def list_tickets(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'baseapp/list_tickets.html', {'tickets': tickets})

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser)
def accept_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.accepted = True
    ticket.save()
    messages.success(request, "Ticket Accepted!!")
    return redirect('baseapp:list_tickets')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser)
def decline_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    messages.info(request, "Ticket Declined!!")
    return redirect('baseapp:list_tickets')

@login_required(login_url='signin')
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'closed'
    ticket.save()
    messages.warning(request, "Ticket Closed!!")
    return redirect('baseapp:list_tickets')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser)
def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        staff_member_id = request.POST.get('staff_member')
        if staff_member_id:
            ticket.assigned_to_id = staff_member_id
            ticket.save()
            return redirect('list_tickets')
    return render(request, 'baseapp/assign_ticket.html', {'ticket': ticket})

@login_required(login_url='signin')
def productsForSale(request):
    products = Accessories.objects.all
    return render(request, 'baseapp/products_for_sale.html', {'products':products})

@login_required(login_url='signin')
def animal_detail(request, id):
    if request.user.is_authenticated:  # Check if user is authenticated
        if hasattr(request.user, 'id'):  # Check if user has 'id' attribute
            print("User ID:", request.user.id)
        else:
            print("User has no 'id' attribute")
    else:
        print("User is not authenticated")

    animal = get_object_or_404(Animal, id=id)

    return render(request, 'baseapp/animal_detail.html', {'animal': animal,'user': request.user})

@login_required(login_url='signin')
def animal_detail_2(request, id):
    if request.user.is_authenticated:  # Check if user is authenticated
        if hasattr(request.user, 'id'):  # Check if user has 'id' attribute
            print("User ID:", request.user.id)
        else:
            print("User has no 'id' attribute")
    else:
        print("User is not authenticated")

    animal = get_object_or_404(Animal, id=id)

    return render(request, 'baseapp/animal_detail_2.html', {'animal': animal,'user': request.user})


@login_required(login_url='signin')
def request_adoption(request, id):
    # Fetch the animal object by its ID
    animal = get_object_or_404(Animal, id=id)
    # Logic to handle adoption request
    # For example, you might want to notify the admin or perform other actions
    messages.success(request, "Adoption Request Successful")
    
# Redirect to a success page or to the animal detail page
    redirect('baseapp:animal_detail', id=id)
    
    return render(request, 'baseapp/animal_detail.html')

# views.py

from django.db.models import Q


@login_required(login_url='signin')
def productsForSale(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    per_page = request.GET.get('per_page', request.session.get('per_page', 10))  # Default to 10 if not provided

    if query is None:
        products = Accessories.objects.all()
    else:
        multiple_q = Q(Q(title__icontains=query) | Q(description__icontains=query))
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

    request.session['per_page'] = per_page  # Remember the user's choice in the session
    paginator = Paginator(products, int(per_page))  # Cast to int because session returns a string

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'query': query,
        'sort_by': sort_by,
        'per_page': per_page
    }

    if query is None:
        return render(request, 'baseapp/products_for_sale.html', context)
    else:
        return render(request, 'baseapp/productsearch.html', context)



def add_to_cart(request, accessory_id):
    if request.method == "POST":
        print(request.POST)
        accessory = get_object_or_404(Accessories, id=accessory_id)
        if accessory.stock < 1:
            messages.error(request, "Out of stock.")
            return redirect('baseapp:products_for_sale')
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, accessory=accessory)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('baseapp:cart')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('baseapp:cart')


def adjust_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if action == "add":
        cart_item.quantity += 1
    elif action == "subtract":
        cart_item.quantity -= 1
        if cart_item.quantity < 1:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
            return redirect('cart_detail')
    cart_item.save()
    messages.success(request, "Cart updated.")
    return redirect('baseapp:cart')


def cart_view(request):
    print(request.user)
    try:
        cart = Cart.objects.get(user=request.user)
        print(cart)
        items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.accessory.price * item.quantity for item in items)
    except Cart.DoesNotExist:
        print("Cart does not exist")
        items = []
        total_price = 0

    context = {
        'items': items,
        'total_price': total_price
    }
    return render(request, 'baseapp/cart.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Accessories, pk=pk)

    return render(request, 'baseapp/product_detail.html', {'product': product})


def place_order(request):
    if request.method == 'POST':
        # Create a new order with form data
        new_order = Order()
        new_order.order_id = generate_random_identifier()  # Generate a random Order ID
        new_order.user = request.user
        cart_items = CartItem.objects.filter(cart__user=request.user)
        new_order.items_summary = "\n".join(
            f"{item.quantity}x {item.accessory.title} - ${item.total_price}" for item in cart_items)
        new_order.total_cost = sum(item.total_price for item in cart_items)
        new_order.name = request.POST.get('name')
        new_order.email = request.POST.get('email')
        new_order.phone = request.POST.get('phone')
        new_order.city = request.POST.get('city')
        new_order.state = request.POST.get('state')
        new_order.address = request.POST.get('address')
        new_order.payment_status = False  # Payment status is initially False
        new_order.payment = request.POST.get('payment')
        new_order.save()
        # Clear the user's cart
        CartItem.objects.filter(cart__user=request.user).delete()
        # Redirect to a new URL for order confirmation
        return redirect('baseapp:order_status', order_id=new_order.id)
        #return redirect('order_confirmation', order_id=new_order.order_id)
    else:
        # If the request is GET, display the cart items and total price
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_price = sum(item.total_price for item in cart_items)

        return render(request, 'baseapp/place_order.html', {'items': cart_items, 'total_price': total_price})

def order_history(request, username):
    #orders = Order.objects.filter(user__username=username)  # Ensure you're filtering by the related user's username
    orders = Order.objects.filter(user__username=username).order_by('-created_at')
    return render(request, 'baseapp/order_history.html', {'orders': orders})

def order_status(request, order_id):
    # Retrieve the order using the order_id
    order = get_object_or_404(Order, id=order_id)
    # Pass the order to the template
    return render(request, 'baseapp/order_status.html', {'order': order})
    
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order Cancelled Successfully!!")
    return redirect('baseapp:order_history', username=request.user.username)

#STRIPE
# views.py
def payment_success(request, order_id):
    # Logic to handle successful payment
    order = get_object_or_404(Order, id=order_id)
    if not order.payment_status:
        order.payment_status=True
        order.save()
    # You can retrieve the session ID with request.GET.get('session_id')
    return render(request, 'baseapp/success.html')

def payment_cancel(request, order_id):
    # Logic to handle payment cancellation
    return render(request, 'baseapp/cancel.html')

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.payment_status:
        # Split the items_summary by line breaks to process each item
        items = order.items_summary.split('\n')
        line_items = []
        for item in items:
            # Assuming each item follows the format "quantityx title - $total_price"
            parts = item.split(' - $')
            quantity, title = parts[0].split('x ')
            total_price = parts[1]
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': title.strip(),
                        #'description': item
                    },
                    'unit_amount': int(float(total_price) * 100/int(quantity.strip())),
                },
                'quantity': int(quantity.strip()),
            })

        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            client_reference_id=order.id,
            success_url=request.build_absolute_uri(reverse('baseapp:payment_success', args=[order.id])),
            cancel_url=request.build_absolute_uri(reverse('baseapp:payment_cancel', args=[order.id])),
        )
        return redirect(session.url, code=303)
    else:
        return redirect('baseapp:order_status', order_id=order.id)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'your-endpoint-secret'  # Replace with your endpoint's secret

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Retrieve the order using the session ID
        order_id = session.get('client_reference_id')
        order = Order.objects.get(id=order_id)

        # Update the order's payment status
        order.payment_status = True
        order.save()

    return HttpResponse(status=200)

from django.shortcuts import render
import requests
@login_required(login_url='signin')
def animal_info(request):
    # Initialize variables
    animal_name = ''
    api_response = ''

    # Check if the form is submitted
    if request.method == 'POST':
        # Extract the animal name from the form
        animal_name = request.POST.get('animal_name', '')

        # Construct the API URL with the provided animal name
        api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(animal_name)

        # Make the API call
        response = requests.get(api_url, headers={'X-Api-Key': 'kwD3sIgglP8eFSY7kT8CLA==pxqZsePmFRhympw6'})

        # Check the response status
        if response.status_code == requests.codes.ok:
            # If successful, get the API response
            api_response = response.json()
        else:
            # If there's an error, display the error message
            api_response = {'error': 'Error occurred while fetching data'}

    # Render the template with the form and API response
    return render(request, 'baseapp/animal_info.html', {'animal_name': animal_name, 'api_response': api_response})

@login_required(login_url='signin')
def know_before(request):
    return render(request, 'baseapp/know_before.html')

@login_required(login_url='signin')
def know_before_cat(request):
    if request.method == 'POST':
        name = request.POST.get('cat_name')  # Get the value of 'cat_name' from the form
        api_url = 'https://api.api-ninjas.com/v1/cats?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': 'kwD3sIgglP8eFSY7kT8CLA==pxqZsePmFRhympw6'})
        if response.status_code == requests.codes.ok:
            api_response = response.json()
            return render(request, 'baseapp/know_before_cat.html', {'api_response': api_response})
        else:
            error_message = "Error: {} {}".format(response.status_code, response.text)
            return render(request, 'baseapp/know_before_cat.html', {'error_message': error_message})
    else:
            # Render an empty form when the page is initially loaded
        return render(request, 'baseapp/know_before_cat.html')
    
@login_required(login_url='signin')
def know_before_dog(request):
    if request.method == 'POST':
        name = request.POST.get('dog_name')  # Get the value of 'cat_name' from the form
        api_url = 'https://api.api-ninjas.com/v1/dogs?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': 'kwD3sIgglP8eFSY7kT8CLA==pxqZsePmFRhympw6'})
        if response.status_code == requests.codes.ok:
            api_response = response.json()
            return render(request, 'baseapp/know_before_dog.html', {'api_response': api_response})
        else:
            error_message = "Error: {} {}".format(response.status_code, response.text)
            return render(request, 'baseapp/know_before_dog.html', {'error_message': error_message})
    else:
            # Render an empty form when the page is initially loaded
        return render(request, 'baseapp/know_before_dog.html')
