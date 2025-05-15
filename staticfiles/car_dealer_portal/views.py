from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from car_dealer_portal.models import *
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings

from car_dealer_portal.models import *
from customer_portal.models import Orders  # jeśli Orders jest w customer_portal
# UWAGA: import Orders, jeśli tam go przechowujesz

from django.core import signing  # do tokenów
# Create your views here.

def send_fake_email(to_email, subject, message):
    """
    Helper: wysyła 'mail' na console (fake).
    Można to zmienić na prawdziwe send_mail().
    """
    # Jeśli używasz EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # to mail pojawi się w konsoli.
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # np. "no-reply@domain.com"
        [to_email],
        fail_silently=False,
    )

def generate_token(data_dict, max_age=3600):
    """
    Tworzy podpisany token (ważny np. 1h).
    """
    return signing.dumps(data_dict, salt='car-dealer-portal')

def verify_token(token, max_age=3600):
    """
    Odczytuje token, zwraca oryginalny słownik data_dict lub None jeśli token nieważny/wygasł.
    """
    try:
        data = signing.loads(token, salt='car-dealer-portal', max_age=max_age)
        return data
    except Exception:
        return None

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'car_dealer/login.html')
    else:
        return render(request, 'car_dealer/home_page.html')

def login(request):
    return render(request, 'car_dealer/login.html')


def auth_view(request):
    # Jeśli user już zalogowany, wyświetlamy np. stronę główną dealera
    if request.user.is_authenticated:
        return render(request, 'car_dealer/home_page.html')

    # Pobieramy dane z POST i usuwamy ewentualne spacje na bokach
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    # Sprawdzamy, czy user/password są wypełnione
    if not username or not password:
        return render(request, 'car_dealer/login_failed.html', {'error_type': 'empty_fields'})

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Sprawdzamy, czy konto jest aktywne
        if not user.is_active:
            return render(request, 'car_dealer/login_failed.html', {'error_type': 'not_active'})
        # Czy jest powiązane z CarDealer?
        try:
            car_dealer = CarDealer.objects.get(car_dealer=user)
        except CarDealer.DoesNotExist:
            car_dealer = None

        if car_dealer is not None:
            auth.login(request, user)
            return render(request, 'car_dealer/home_page.html')
        else:
            return render(request, 'car_dealer/login_failed.html', {'error_type': 'no_dealer'})
    else:
        # Rozróżniamy: user istnieje, ale hasło złe, czy user nie istnieje?
        if User.objects.filter(username=username).exists():
            error_type = 'wrong_password'
        else:
            error_type = 'no_user'

        return render(request, 'car_dealer/login_failed.html', {'error_type': error_type})


def logout_view(request):
    auth.logout(request)
    return render(request, 'car_dealer/login.html')

def register(request):
    return render(request, 'car_dealer/register.html')

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip().lower()
        pincode = request.POST.get('pincode', '').strip()

        errors = {}

        # Walidacja imion (tylko litery)
        if not firstname.isalpha():
            errors['firstname'] = "First name can only contain letters."
        if not lastname.isalpha():
            errors['lastname'] = "Last name can only contain letters."

        # Walidacja username
        if len(username) < 5:
            errors['username'] = "Username must be at least 5 characters long."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists. Please choose another."

        # Walidacja hasła
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        # Walidacja email
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format."

        # Walidacja telefonu
        if not mobile.isdigit() or len(mobile) not in [10, 13]:
            errors['mobile'] = "Contact number must be a valid 10-13 digit number."


        if User.objects.filter(email=email).exists():
            errors['email'] = "This email is already in use by another account."

        if errors:
            return render(
                request,
                'car_dealer/register.html',
                {
                    'errors': errors,
                    'data': request.POST
                }
            )

        # Tworzymy użytkownika, ale is_active = False
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            user.is_active = False
            user.save()
        except:
            return render(request, 'car_dealer/registration_error.html')

        area = None
        if city and pincode:
            area, _ = Area.objects.get_or_create(city=city, pincode=pincode)

        car_dealer = CarDealer(car_dealer=user, mobile=mobile, area=area)
        car_dealer.save()

        # Generujemy token do aktywacji
        token_data = {'user_id': user.id}
        token = generate_token(token_data, max_age=3600)  # ważny 1h

        # Tworzymy link aktywacyjny
        activation_link = request.build_absolute_uri(f"/car_dealer_portal/activate/{token}/")

        subject = "Activate your Dealer account"
        message = (
            f"Hello {firstname},\n\n"
            f"Thank you for registering. Please click the link below to activate your account:\n"
            f"{activation_link}\n\n"
            "If you did not request this registration, please ignore this email."
        )

        # Wysyłamy mail aktywacyjny
        send_fake_email(email, subject, message)

        # Przekieruj na stronę, że email wysłany
        return render(request, 'car_dealer/registration_pending.html')
    else:
        return render(request, 'car_dealer/register.html')


def activate_account(request, token):
    data = verify_token(token, max_age=3600)
    if data is None:
        # Token nieważny lub wygasł
        return render(request, 'car_dealer/activation_failed.html')

    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return render(request, 'car_dealer/activation_success.html')
    except User.DoesNotExist:
        return render(request, 'car_dealer/activation_failed.html')

def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        # Szukamy usera z danym emailem
        try:
            user = User.objects.get(email=email)
            # Generuj token
            token_data = {'user_id': user.id}
            token = generate_token(token_data, max_age=3600)  # 1h
            reset_link = request.build_absolute_uri(f"/car_dealer_portal/reset_password_confirm/{token}/")

            subject = "Dealer Password Reset"
            message = (
                f"Hello {user.first_name},\n\n"
                f"Please click the link below to reset your password:\n"
                f"{reset_link}\n\n"
                "If you did not request a password reset, ignore this email."
            )
            send_fake_email(email, subject, message)

            return render(request, 'car_dealer/reset_password_email_sent.html')
        except User.DoesNotExist:
            # Nie zdradzamy, że email nie istnieje – uniwersalny komunikat
            return render(request, 'car_dealer/reset_password_email_sent.html')
    else:
        return render(request, 'car_dealer/reset_password_request.html')

def reset_password_confirm(request, token):
    data = verify_token(token, max_age=3600)
    if data is None:
        return render(request, 'car_dealer/activation_failed.html')

    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'car_dealer/activation_failed.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if len(new_password) < 8:
            error = "Password must be at least 8 characters long."
            return render(request, 'car_dealer/reset_password_confirm.html', {'error': error, 'token': token})

        if new_password != confirm_password:
            error = "Passwords do not match."
            return render(request, 'car_dealer/reset_password_confirm.html', {'error': error, 'token': token})

        # OK – zmieniamy hasło
        user.set_password(new_password)
        user.save()
        return render(request, 'car_dealer/password_reset_success.html')
    else:
        return render(request, 'car_dealer/reset_password_confirm.html', {'token': token})

@login_required
def update_profile(request):
    """
    Zmiana:
    - username
    - mobile
    - city
    - pincode
    Walidacja analogiczna do rejestracji.
    """
    user = request.user
    try:
        car_dealer = CarDealer.objects.get(car_dealer=user)
    except CarDealer.DoesNotExist:
        return HttpResponse("No CarDealer profile found.", status=404)

    if request.method == "POST":
        new_username = request.POST.get('username', '').strip()
        new_mobile = request.POST.get('mobile', '').strip()
        new_city = request.POST.get('city', '').strip().lower()
        new_pincode = request.POST.get('pincode', '').strip()
        errors = {}

        # Walidacja username
        if len(new_username) < 5:
            errors['username'] = "Username must be at least 5 characters long."
        else:
            # Sprawdzamy, czy jest wolna (ale wykluczamy własnego usera)
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                errors['username'] = "This username is already taken."

        # Walidacja mobile
        if not new_mobile.isdigit() or len(new_mobile) not in [10, 13]:
            errors['mobile'] = "Contact number must be 10-13 digits."

        # Tworzenie/pobieranie area
        area_instance = None
        if new_city and new_pincode:
            area_instance, _ = Area.objects.get_or_create(city=new_city, pincode=new_pincode)
        elif (not new_city) and (not new_pincode):
            # Możemy pozwolić na wyczyszczenie area
            area_instance = None
        else:
            # Podał city ale brak pincode lub odwrotnie
            errors['area'] = "Both city and pincode must be provided together."

        if errors:
            return render(request, 'car_dealer/update_profile.html', {
                'errors': errors,
                'data': request.POST
            })

        # Jeśli brak błędów, zapisujemy
        user.username = new_username
        user.save()

        car_dealer.mobile = new_mobile
        car_dealer.area = area_instance
        car_dealer.save()

        return render(request, 'car_dealer/profile_updated.html')
    else:
        # Metoda GET – pokaż formularz z aktualnymi danymi
        context = {
            'data': {
                'username': user.username,
                'mobile': car_dealer.mobile,
                'city': car_dealer.area.city if car_dealer.area else '',
                'pincode': car_dealer.area.pincode if car_dealer.area else '',
            }
        }
        return render(request, 'car_dealer/update_profile.html', context)

@login_required
def add_vehicle(request):
    cd = CarDealer.objects.get(car_dealer=request.user)

    car_name = request.POST['car_name'].strip()
    color = request.POST['color'].strip()
    city = request.POST['city'].strip().lower()
    pincode = request.POST['pincode'].strip()
    description = request.POST['description'].strip()
    capacity = request.POST['capacity'].strip()
    price = request.POST['price'].strip()

    # Tutaj odbieramy plik:
    photo_file = request.FILES.get('photo')  # None, jeśli brak załącznika

    errors = {}
    if not car_name:
        errors['car_name'] = "Car name is required."
    if not color:
        errors['color'] = "Color is required."
    if not city:
        errors['city'] = "City is required."
    if not pincode or not pincode.isdigit() or len(pincode) != 6:
        errors['pincode'] = "Pincode must be a 6-digit number."
    if not capacity.isdigit() or int(capacity) <= 0:
        errors['capacity'] = "Capacity must be a positive number."
    if not price.isdigit() or int(price) < 0:
        errors['price'] = "Price must be a non-negative number."
    if errors:
        return render(request, 'car_dealer/home_page.html', {
            'form_errors': errors,
            'form_data': request.POST
        })
    # Szukamy/ tworzymy obiekt Area
    try:
        area, created = Area.objects.get_or_create(city=city, pincode=pincode)
    except IntegrityError:
        # This handles the case where the unique_together constraint is violated
        errors['pincode'] = "This pincode is already associated with another city."
        return render(request, 'car_dealer/home_page.html', {
            'form_errors': errors,
            'form_data': request.POST
        })

    # Tworzymy pojazd
    car = Vehicles(
        car_name=car_name,
        color=color,
        dealer=cd,
        area=area,
        description=description,
        capacity=capacity,
        price=int(price),
    )
    # Jeśli jest plik – przypisz go do field:
    if photo_file:
        car.photo = photo_file

    car.save()

    return render(request, 'car_dealer/vehicle_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = car_dealer)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'car_dealer/manage.html', {'vehicle_list':vehicle_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'car_dealer/order_list.html', {'order_list':order_list})

@login_required
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    order.is_complete = True
    order.save()
    vehicle.is_available = True
    vehicle.save()
    return HttpResponseRedirect('/car_dealer_portal/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'car_dealer/history.html', {'wallet':car_dealer.wallet, 'order_list':order_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    vehicle = Vehicles.objects.get(id=veh_id)
    # ewentualnie sprawdzamy, czy user to właściciel
    if vehicle.dealer.car_dealer != request.user:
        return HttpResponse("You do not own this vehicle.", status=403)

    vehicle.delete()
    return HttpResponseRedirect('/car_dealer_portal/manage_vehicles/')

@login_required
def vehicle_detail(request, vehicle_id):
    """Widok szczegółów pojazdu."""
    user = request.user
    try:
        vehicle = Vehicles.objects.get(id=vehicle_id)
    except Vehicles.DoesNotExist:
        return HttpResponse("Vehicle not found.", status=404)

    # Sprawdzenie, czy to na pewno pojazd tego dealera:
    if vehicle.dealer.car_dealer != user:
        return HttpResponse("You do not own this vehicle.", status=403)

    context = {
        'vehicle': vehicle
    }
    return render(request, 'car_dealer/vehicle_detail.html', context)

@login_required
def confirm_delete_vehicle(request, vehicle_id):
    """
    Wyświetla stronę potwierdzenia, a dopiero po kliknięciu potwierdzenia
    rzeczywiście usuwa pojazd w innym widoku/funkcji.
    """
    user = request.user
    try:
        vehicle = Vehicles.objects.get(id=vehicle_id)
    except Vehicles.DoesNotExist:
        return HttpResponse("Vehicle not found.", status=404)

    if vehicle.dealer.car_dealer != user:
        return HttpResponse("You do not own this vehicle.", status=403)

    return render(request, 'car_dealer/confirm_delete_vehicle.html', {'vehicle': vehicle})

@login_required
def confirm_complete_order(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Sprawdź, czy to order dealera zalogowanego:
    if order.car_dealer.car_dealer != request.user:
        return HttpResponse("You do not own this order", status=403)

    # order zawiera vehicle, user, rent, days...
    # Możemy wyświetlić info o kliencie (np. order.user.first_name).
    return render(request, 'car_dealer/confirm_complete_order.html', {'order': order})

@login_required
def order_detail(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        return HttpResponse("Order not found", status=404)

    # Sprawdź, czy należy do zalogowanego dealera:
    if order.car_dealer.car_dealer != request.user:
        return HttpResponse("You do not own this order", status=403)

    context = {'order': order}
    return render(request, 'car_dealer/order_detail.html', context)
