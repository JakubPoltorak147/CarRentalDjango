from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.core import signing
from django.core.mail import send_mail
from django.conf import settings

from customer_portal.models import Customer,Orders
from car_dealer_portal.models import Area, Vehicles

#################
# HELPER FUNCTIONS
#################

def send_fake_email(to_email, subject, message):
    """
    Helper: wysyła 'mail' na console (fake).
    Możesz to zmienić na send_mail() z EMAIL_BACKEND console,
    lub inny backend.
    """
    # W przypadku console backend wystarczy:
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )
    # Spowoduje to wypisanie maila w konsoli, o ile EMAIL_BACKEND=console.


def generate_token(data_dict, max_age=3600):
    """
    Tworzy podpisany token na podstawie data_dict
    max_age – ważność w sekundach (np. 1h)
    """
    return signing.dumps(data_dict, salt='customer-portal')


def verify_token(token, max_age=3600):
    """
    Odczytuje token, zwraca oryginalny słownik data_dict lub None jeśli nieważny.
    """
    try:
        data = signing.loads(token, salt='customer-portal', max_age=max_age)
        return data
    except Exception:
        return None

#################
# INDEX, LOGIN, LOGOUT
#################

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'customer/login.html')
    else:
        return render(request, 'customer/home_page.html')

def login(request):
    return render(request, 'customer/login.html')

def auth_view(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    # Blokada pustych pól:
    if not username or not password:
        # Możesz zrobić np.:
        return render(request, 'customer/login_failed.html', {'error_type': 'empty_fields'})

    user = authenticate(request, username=username, password=password)

    if user is not None:  # Użytkownik został uwierzytelniony poprawnie
        # Sprawdź czy user jest aktywny:
        if not user.is_active:
            return render(request, 'customer/login_failed.html', {'error_type': 'not_active'})

        try:
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            customer = None

        if customer is not None:
            auth.login(request, user)
            return render(request, 'customer/home_page.html')
        else:
            # Jeśli użytkownik nie jest przypisany do modelu Customer
            return render(request, 'customer/login_failed.html', {'error_type': 'no_customer'})
    else:
        # Rozróżnij brak użytkownika i błędne hasło
        if User.objects.filter(username=username).exists():
            error_type = 'wrong_password'  # Użytkownik istnieje, ale hasło jest błędne
        else:
            error_type = 'no_user'  # Użytkownik o podanym username nie istnieje

        return render(request, 'customer/login_failed.html', {'error_type': error_type})

def logout_view(request):
    auth.logout(request)
    return render(request, 'customer/login.html')

def register(request):
    return render(request, 'customer/register.html')

def registration(request):
    if request.method == "POST":
        # Pobranie danych z formularza
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        age = request.POST.get('age', '').strip()
        license_number = request.POST.get('license', '').strip()

        # Słownik na błędy
        errors = {}

        # Walidacja imienia i nazwiska
        if not firstname.isalpha():
            errors['firstname'] = "First name can only contain letters."
        if not lastname.isalpha():
            errors['lastname'] = "Last name can only contain letters."

        # Walidacja nazwy użytkownika
        if len(username) < 5:
            errors['username'] = "Username must be at least 5 characters long."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Username already exists. Please choose another."

        # Walidacja hasła
        if len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."

        # Walidacja emaila
        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Invalid email format."

        # Walidacja numeru telefonu
        if not mobile.isdigit() or len(mobile) not in [10, 13]:
            errors['mobile'] = "Contact number must be a valid 10-13 digit number."

        # Jeśli są błędy, wróć do formularza z błędami i danymi
        if errors:
            return render(
                request,
                'customer/register.html',
                {
                    'errors': errors,
                    'data': request.POST  # przekazujemy też wpisane dane
                }
            )

        # Tworzenie użytkownika i klienta (na razie nieaktywny!)
        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            # Ustawiamy is_active=False i zapisujemy:
            user.is_active = False
            user.save()

            # Jeżeli podano city i pincode - utwórz lub pobierz area
            area_instance = None
            if city and pincode:
                area_instance, _ = Area.objects.get_or_create(
                    city=city.lower(),
                    pincode=pincode
                )

            # Konwersja age do int, jeżeli podano
            final_age = None
            if age.isdigit():
                final_age = int(age)

            customer = Customer(
                user=user,
                mobile=mobile,
                area=area_instance,
                age=final_age,
                license_number=license_number
            )
            customer.save()

            # Wygeneruj token aktywacyjny i wyślij mailem
            token_data = {'user_id': user.id}
            token = generate_token(token_data)

            activation_link = request.build_absolute_uri(
                f"/customer_portal/activate/{token}/"
            )
            subject = "Activate your account"
            message = (
                f"Hello {firstname},\n\n"
                f"Thank you for registering. Please click the link below to activate your account:\n"
                f"{activation_link}\n\n"
                "If you did not request this registration, please ignore this email."
            )

            send_fake_email(user.email, subject, message)

            # Strona, że wysłano mail aktywacyjny
            return render(request, 'customer/registration_pending.html')

        except Exception as e:
            errors['general'] = (
                "An error occurred during registration. "
                "Please try again or contact support."
            )
            return render(
                request,
                'customer/register.html',
                {'errors': errors, 'data': request.POST}
            )
    else:
        return render(request, 'customer/register.html')

def activate_account(request, token):
    # Odczytanie tokenu
    data = verify_token(token)
    if data is None:
        return render(request, 'customer/activation_failed.html')

    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return render(request, 'customer/account_activated.html')
    except User.DoesNotExist:
        return render(request, 'customer/activation_failed.html')
#################
# RESET PASSWORD
#################

def reset_password_request(request):
    """
    Widok z formularzem, w którym user podaje email,
    aby wygenerować link do zmiany hasła.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        # Wyszukaj usera
        try:
            user = User.objects.get(email=email)
            # Generuj token
            token_data = {'user_id': user.id}
            token = generate_token(token_data)
            reset_link = request.build_absolute_uri(
                f"/customer_portal/reset_password_confirm/{token}/"
            )

            subject = "Password reset"
            message = (
                f"Hello {user.first_name},\n\n"
                f"Please click the link below to reset your password:\n"
                f"{reset_link}\n\n"
                "If you did not request a password reset, ignore this email."
            )

            send_fake_email(email, subject, message)
            return render(request, 'customer/reset_password_email_sent.html')
        except User.DoesNotExist:
            # Nie zdradzamy, że mail nie istnieje – można np. pokazać uniwersalny komunikat
            return render(request, 'customer/reset_password_email_sent.html')
    else:
        return render(request, 'customer/reset_password_request.html')

def reset_password_confirm(request, token):
    """
    Widok, w którym user wklepuje nowe hasło.
    """
    data = verify_token(token)
    if data is None:
        return render(request, 'customer/activation_failed.html')

    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return render(request, 'customer/activation_failed.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if len(new_password) < 8:
            error = "Password must be at least 8 characters long."
            return render(request, 'customer/reset_password_confirm.html', {'error': error, 'token': token})

        if new_password != confirm_password:
            error = "Passwords do not match."
            return render(request, 'customer/reset_password_confirm.html', {'error': error, 'token': token})

        # OK – zmieniamy hasło
        user.set_password(new_password)
        user.save()
        return render(request, 'customer/password_reset_success.html')
    else:
        return render(request, 'customer/reset_password_confirm.html', {'token': token})
@login_required
def update_profile(request):
    """
    Pozwala zmienić:
      - username
      - mobile (Contact Number)
      - city
      - pincode
      - age
    Walidacja jak w rejestracji.
    """
    user = request.user
    customer = Customer.objects.get(user=user)

    errors = {}
    if request.method == "POST":
        new_username = request.POST.get('username', '').strip()
        new_mobile = request.POST.get('mobile', '').strip()
        new_city = request.POST.get('city', '').strip()
        new_pincode = request.POST.get('pincode', '').strip()
        new_age = request.POST.get('age', '').strip()

        # Walidacja username:
        if len(new_username) < 5:
            errors['username'] = "Username must be at least 5 characters long."
        else:
            # Sprawdzamy, czy user już nie istnieje i to nie my
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                errors['username'] = "Username already exists. Please choose another."

        # Walidacja mobilnego:
        if not new_mobile.isdigit() or len(new_mobile) not in [10, 13]:
            errors['mobile'] = "Contact number must be a valid 10-13 digit number."

        # Walidacja city + pincode -> dowolna logika
        # Np. nic szczególnego, ale jeśli user coś poda,
        # można spróbować get_or_create area:
        area_instance = None
        if new_city and new_pincode:
            area_instance, _ = Area.objects.get_or_create(
                city=new_city.lower(),
                pincode=new_pincode
            )

        # Walidacja age (opcjonalnie)
        final_age = None
        if new_age:
            if not new_age.isdigit():
                errors['age'] = "Age must be a number."
            else:
                final_age = int(new_age)

        if errors:
            return render(request, 'customer/update_profile.html', {
                'errors': errors,
                'data': request.POST,
            })

        # Jeśli brak błędów – zapisujemy
        user.username = new_username
        user.save()

        customer.mobile = new_mobile
        customer.age = final_age
        if area_instance:
            customer.area = area_instance
        elif not new_city and not new_pincode:
            # Pozwalamy np. na usunięcie area
            customer.area = None
        customer.save()

        return render(request, 'customer/profile_updated.html')
    else:
        # GET – wyświetlamy formularz z aktualnymi danymi
        context = {
            'data': {
                'username': user.username,
                'mobile': customer.mobile,
                'city': customer.area.city if customer.area else '',
                'pincode': customer.area.pincode if customer.area else '',
                'age': customer.age if customer.age else '',
            }
        }
        return render(request, 'customer/update_profile.html', context)

@login_required
def search(request):
    return render(request, 'customer/search.html')

@login_required
def search_results(request):
    # Pobieramy z formularza nazwę parametru i wartość wyszukiwania
    param = request.POST.get('parameter', '').strip()
    query = request.POST.get('query', '').strip().lower()

    # Domyślnie pusta lista lub queryset
    vehicles = Vehicles.objects.none()

    if param == 'city':
        # Szukamy w polu city powiązanej tabeli Area
        areas = Area.objects.filter(city__icontains=query)
        vehicles = Vehicles.objects.filter(area__in=areas, is_available=True)

    elif param == 'color':
        vehicles = Vehicles.objects.filter(color__icontains=query, is_available=True)

    elif param == 'capacity':
        # capacity to pole typu int; jeśli user poda liczbę, próbujemy ją dopasować
        # lub np. 'capacity__gte=query' – zależnie od logiki
        if query.isdigit():
            vehicles = Vehicles.objects.filter(capacity=query, is_available=True)

    elif param == 'car_name':
        vehicles = Vehicles.objects.filter(car_name__icontains=query, is_available=True)

    # Przekazujemy do szablonu param i query, żeby wyświetlić co wpisano
    return render(request, 'customer/search_results.html', {
        'vehicles': vehicles,
        'param': param,
        'query': query
    })


@login_required
def rent_vehicle(request):
    id = request.POST['id']
    vehicle = Vehicles.objects.get(id = id)
    cost_per_day = int(vehicle.price)
    return render(request, 'customer/confirmation.html', {'vehicle':vehicle, 'cost_per_day':cost_per_day})

@login_required
def confirm(request):
    vehicle_id = request.POST['id']
    username = request.user
    user = User.objects.get(username = username)
    days_str = request.POST.get('days', '').strip()
    if not days_str.isdigit() or int(days_str) < 1:
        # Możesz przekierować z powrotem do confirmation.html
        # lub wyświetlić jakiś błąd
        return render(request, 'customer/order_failed.html', {
            'error_message': "Invalid number of days."
        })

    days = int(days_str)
    vehicle = Vehicles.objects.get(id = vehicle_id)
    if vehicle.is_available:
        car_dealer = vehicle.dealer
        rent = int(vehicle.price)*days
        car_dealer.wallet += rent
        car_dealer.save()
        try:
            order = Orders(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
        vehicle.is_available = False
        vehicle.save()
        return render(request, 'customer/confirmed.html', {'order':order})
    else:
        return render(request, 'customer/order_failed.html')

@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user = user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if o.is_complete == False:
                order_dictionary = {'id':o.id,'rent':o.rent, 'vehicle':o.vehicle, 'days':o.days, 'car_dealer':o.car_dealer}
                order_list.append(order_dictionary)
    return render(request, 'customer/manage.html', {'od':order_list})

@login_required
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    order.delete()
    cost_per_day = int(vehicle.capacity)*13
    return render(request, 'customer/confirmation.html', {'vehicle':vehicle}, {'cost_per_day':cost_per_day})

@login_required
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    order.delete()
    return HttpResponseRedirect('/customer_portal/manage/')


def login_failed_view(request, error_type):
    return render(request, 'customer/login_failed.html', {'error_type': error_type})

@login_required
def all_cars(request):
    # Możesz wyświetlać tylko dostępne samochody:
    vehicles = Vehicles.objects.filter(is_available=True)
    # Albo wszystkie:
    # vehicles = Vehicles.objects.all()
    return render(request, 'customer/all_cars.html', {'vehicles': vehicles})

@login_required
def vehicle_details(request, vehicle_id):
    vehicle = get_object_or_404(Vehicles, id=vehicle_id)

    context = {
        'vehicle': vehicle
    }
    return render(request, 'customer/vehicle_details.html', context)


@login_required
def order_detail(request, order_id):
    # Pobierz zamówienie lub zwróć 404, jeśli nie istnieje
    order = get_object_or_404(Orders, id=order_id, user=request.user)

    context = {
        'order': order
    }
    return render(request, 'customer/order_detail.html', context)