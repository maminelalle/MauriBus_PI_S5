from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User as DjangoUser

from rest_framework.authtoken.models import Token
import json

from .models import Bus, Line, Trip, Driver, User, Message


# ---------- Login Admin ----------
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("mauribus_app:dashboard")

    error = None
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("mauribus_app:dashboard")
        else:
            error = "Invalid credentials"

    return render(request, "admin/login.html", {"error": error})

# ---------- Logout ----------
def admin_logout(request):
    logout(request)
    return redirect("mauribus_app:login")


# ---------- Driver Login & Views ----------
def driver_login(request):
    # Allow login by driver name or matricule (id) + phone
    error = None
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        phone = request.POST.get('phone', '').strip()
        driver = None
        if identifier.isdigit():
            driver = Driver.objects.filter(id=int(identifier), phone=phone).first()
        if not driver:
            driver = Driver.objects.filter(name__iexact=identifier, phone=phone).first()
        if driver:
            # login the related user
            login(request, driver.user)
            return redirect('mauribus_app:driver_dashboard')
        else:
            error = 'Identifiants invalides'
    return render(request, 'driver/login.html', {'error': error})


@never_cache
def driver_logout(request):
    logout(request)
    return redirect('mauribus_app:driver_login')


def _require_driver(func):
    # decorator to ensure user is a driver
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_driver', False):
            return redirect('mauribus_app:driver_login')
        return func(request, *args, **kwargs)
    return wrapper


def _require_citizen(func):
    # decorator to ensure user is a citizen
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_citizen', False):
            return redirect('mauribus_app:citizen_login')
        return func(request, *args, **kwargs)
    return wrapper


@never_cache
@_require_driver
@never_cache
@_require_driver
def driver_dashboard(request):
    # Basic stats and lines for map
    from django.utils import timezone
    today = timezone.now().date()
    trips_today = Trip.objects.filter(date__date=today, bus__driver__user=request.user).count()
    trips_assigned = Trip.objects.filter(bus__driver__user=request.user).count()
    completed = Trip.objects.filter(bus__driver__user=request.user, date__lt=timezone.now()).count()
    ongoing = trips_assigned - completed
    recent_trips = Trip.objects.filter(bus__driver__user=request.user).select_related('bus', 'line').order_by('-date')[:5]
    lines = Line.objects.filter(trip__bus__driver__user=request.user).distinct()
    now = timezone.now()
    return render(request, 'driver/dashboard.html', {
        'trips_today': trips_today,
        'trips_assigned': trips_assigned,
        'trips_completed': completed,
        'trips_ongoing': ongoing,
        'recent_trips': recent_trips,
        'lines': lines,
        'now': now,
    })


@never_cache
@_require_driver
def driver_trips(request):
    from django.utils import timezone
    trips = Trip.objects.filter(bus__driver__user=request.user).select_related('bus', 'line')
    return render(request, 'driver/trips.html', {'trips': trips, 'now': timezone.now()})


@never_cache
@_require_driver
def driver_action(request):
    # handle start/complete/report actions from drivers
    if request.method != 'POST':
        return redirect('mauribus_app:driver_trips')
    action = request.POST.get('action')
    trip_id = request.POST.get('trip_id')
    from django.utils import timezone
    if not trip_id:
        return redirect('mauribus_app:driver_trips')
    try:
        trip = Trip.objects.get(id=trip_id, bus__driver__user=request.user)
    except Trip.DoesNotExist:
        return redirect('mauribus_app:driver_trips')

    if action == 'start':
        trip.status = 'started'
        trip.started_at = timezone.now()
        trip.save()
    elif action == 'complete':
        trip.status = 'completed'
        trip.completed_at = timezone.now()
        trip.save()
    elif action == 'report':
        # create message to admin
        content = request.POST.get('report_message', '').strip()
        if content:
            Message.objects.create(sender=request.user, recipient=None, trip=trip, content=content)
    return redirect('mauribus_app:driver_trips')


@never_cache
@_require_driver
def driver_buses(request):
    buses = Bus.objects.filter(driver__user=request.user)
    return render(request, 'driver/buses.html', {'buses': buses})


@never_cache
@_require_driver
def driver_lines(request):
    # lines assigned via trips/buses
    lines = Line.objects.filter(trip__bus__driver__user=request.user).distinct()
    return render(request, 'driver/lines.html', {'lines': lines})


@never_cache
@_require_driver
def driver_profile(request):
    driver = Driver.objects.filter(user=request.user).first()
    return render(request, 'driver/profile.html', {'driver': driver})


@never_cache
@_require_driver
def driver_notifications(request):
    # placeholder list
    notifications = []
    return render(request, 'driver/notifications.html', {'notifications': notifications})


@never_cache
@_require_driver
def driver_messages(request):
    driver = request.user.driver
    # Get messages sent to this driver (individual messages) or broadcast messages
    messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender', 'trip').order_by('-created_at')
    return render(request, 'driver/messages.html', {'messages': messages})


# ---------- Citizen Login & Views ----------
def citizen_login(request):
    if request.user.is_authenticated and getattr(request.user, 'is_citizen', False):
        return redirect('mauribus_app:citizen_dashboard')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '').strip()
        user = None
        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password) and getattr(user, 'is_citizen', False):
                login(request, user)
                return redirect('mauribus_app:citizen_dashboard')
        error = 'Identifiants invalides'

    return render(request, 'citizen/login.html', {'error': error})


def citizen_register(request):
    if request.user.is_authenticated and getattr(request.user, 'is_citizen', False):
        return redirect('mauribus_app:citizen_dashboard')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not email or not password:
            error = 'Email et mot de passe requis'
        elif password != password2:
            error = 'Les mots de passe ne correspondent pas'
        elif User.objects.filter(email=email).exists():
            error = 'Cet email est déjà utilisé'
        else:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_citizen=True,
                is_driver=False,
                is_staff=False,
            )
            login(request, user)
            return redirect('mauribus_app:citizen_dashboard')

    return render(request, 'citizen/register.html', {'error': error})


@never_cache
def citizen_logout(request):
    logout(request)
    return redirect('mauribus_app:citizen_login')


@never_cache
def citizen_dashboard(request):
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    lines_count = Line.objects.count()
    trips_today = Trip.objects.filter(date__date=today).count()
    trips_total = Trip.objects.count()

    status_labels = {
        'scheduled': ('En service', 'status-ok'),
        'started': ('En cours', 'status-warn'),
        'completed': ('Terminé', 'status-done'),
        'cancelled': ('Suspendu', 'status-stop'),
        'not_completed': ('Suspendu', 'status-stop'),
    }

    trip_cards = []
    trips = Trip.objects.select_related('line', 'bus').order_by('-date')
    for trip in trips:
        arrival_time = None
        duration_minutes = 30
        if trip.date:
            arrival_time = trip.date + timedelta(minutes=duration_minutes)
        label, badge = status_labels.get(trip.status, ('En service', 'status-ok'))
        trip_cards.append({
            'id': trip.id,
            'line_name': trip.line.name,
            'start': trip.line.start,
            'end': trip.line.end,
            'departure': trip.date,
            'arrival': arrival_time,
            'duration': duration_minutes,
            'status_label': label,
            'status_class': badge,
            'start_lat': trip.line.start_lat,
            'start_lng': trip.line.start_lng,
            'end_lat': trip.line.end_lat,
            'end_lng': trip.line.end_lng,
        })

    return render(request, 'citizen/public_dashboard.html', {
        'lines_count': lines_count,
        'trips_today': trips_today,
        'trips_total': trips_total,
        'today': today,
        'trip_cards': trip_cards,
    })


@never_cache
def citizen_lines(request):
    lines = Line.objects.all().order_by('name')
    return render(request, 'citizen/lines.html', {'lines': lines})


@never_cache
def citizen_trips(request):
    trips = Trip.objects.select_related('line', 'bus').order_by('-date')
    return render(request, 'citizen/trips.html', {'trips': trips})


@never_cache
def citizen_trip_detail(request, trip_id):
    trip = Trip.objects.select_related('line', 'bus').filter(id=trip_id).first()
    if not trip:
        return redirect('mauribus_app:citizen_trips')
    return render(request, 'citizen/trip_detail.html', {
        'trip': trip,
        'line': trip.line,
    })


@never_cache
def citizen_profile(request):
    return render(request, 'citizen/profile.html', {'user': request.user})


@login_required
@never_cache
def admin_messages(request):
    # admin view to see and send messages
    if not request.user.is_staff:
        return redirect('mauribus_app:login')
    drivers = Driver.objects.all()
    msgs = Message.objects.select_related('sender', 'recipient', 'trip').order_by('-created_at')
    return render(request, 'admin/messages.html', {'messages': msgs, 'drivers': drivers})


@login_required
@never_cache
def admin_send_message(request):
    if not request.user.is_staff:
        return redirect('mauribus_app:login')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        recipient_id = request.POST.get('recipient')
        broadcast = request.POST.get('broadcast') == '1'
        if content:
            if broadcast:
                Message.objects.create(sender=request.user, recipient=None, content=content, broadcast=True)
            else:
                if recipient_id and recipient_id != 'all':
                    try:
                        recipient = User.objects.get(id=int(recipient_id))
                    except User.DoesNotExist:
                        recipient = None
                    Message.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('mauribus_app:admin_messages')
    return redirect('mauribus_app:admin_messages')

# ---------- Dashboard ----------
from .models import Bus, Line, Trip, Driver, User
@never_cache
@login_required(login_url='mauribus_app:login')
# ---------- Dashboard ----------

def dashboard(request):
    # Handle forms
    if request.method == "POST":

        # ---------- Bus ----------
        if 'name' in request.POST and 'capacity' in request.POST and 'driver' in request.POST:
            bus_id = request.POST.get('bus_id')
            driver_id = request.POST.get('driver')
            status = request.POST.get('status', 'service')

            if bus_id:
                bus = Bus.objects.get(id=bus_id)
                bus.name = request.POST['name']
                bus.capacity = request.POST['capacity']
                bus.driver_id = driver_id if driver_id else None
                bus.status = status
                bus.save()
            else:
                Bus.objects.create(
                    name=request.POST['name'],
                    capacity=request.POST['capacity'],
                    driver_id=driver_id if driver_id else None,
                    status=status
                )
            return redirect("mauribus_app:dashboard")

        # ---------- Line ----------
        elif 'name' in request.POST and 'start' in request.POST and 'end' in request.POST and 'trip_bus_id' not in request.POST:
            line_id = request.POST.get('line_id')

            if line_id:
                line = Line.objects.get(id=line_id)
                line.name = request.POST['name']
                line.start = request.POST['start']
                line.end = request.POST['end']
                line.save()
            else:
                Line.objects.create(
                    name=request.POST['name'],
                    start=request.POST['start'],
                    end=request.POST['end']
                )
            return redirect("mauribus_app:dashboard")

        # ---------- Trip ----------
        elif 'trip_bus_id' in request.POST and 'trip_line_id' in request.POST:
            trip_id = request.POST.get('trip_id')

            if trip_id:
                trip = Trip.objects.get(id=trip_id)
                trip.bus_id = request.POST['trip_bus_id']
                trip.line_id = request.POST['trip_line_id']
                trip.date = request.POST.get('trip_date')
                trip.save()
            else:
                Trip.objects.create(
                    bus_id=request.POST['trip_bus_id'],
                    line_id=request.POST['trip_line_id'],
                    date=request.POST.get('trip_date')
                )
            return redirect("mauribus_app:dashboard")

        # ---------- Driver ----------
        elif 'driver_name' in request.POST:
            driver_id = request.POST.get('driver_id')
            name = request.POST.get('driver_name')
            phone = request.POST.get('phone', '')

            if driver_id:
                driver = Driver.objects.get(id=driver_id)
                driver.name = name
                driver.phone = phone
                driver.save()
            else:
                user = User.objects.create_user(
                    email=f"{name.lower().replace(' ', '_')}@driver.local",
                    password="defaultpass",
                    is_driver=True
                )
                Driver.objects.create(user=user, name=name, phone=phone)

            return redirect("mauribus_app:dashboard")

        # ---------- User ----------
        elif 'email' in request.POST:
            user_id = request.POST.get('user_id')
            email = request.POST.get('email')
            password = request.POST.get('password')
            is_staff = 'is_staff' in request.POST

            if user_id:
                user = User.objects.get(id=user_id)
                user.email = email
                if password:
                    user.set_password(password)
                user.is_staff = is_staff
                user.save()
            else:
                User.objects.create_user(
                    email=email,
                    password=password,
                    is_staff=is_staff
                )

            return redirect("mauribus_app:dashboard")

    # ---------- Render ----------
    return render(request, "admin/dashboard.html", {
        "buses": Bus.objects.count(),
        "lines": Line.objects.count(),
        "trips": Trip.objects.count(),
        "drivers": Driver.objects.count(),
        "users": User.objects.count(),
        "buses_list": Bus.objects.all(),
        "lines_list": Line.objects.all(),
        "trips_list": Trip.objects.select_related("bus", "line"),
        "drivers_list": Driver.objects.all(),
        "users_list": User.objects.all(),
    })

@never_cache
@login_required
def bus_delete(request, bus_id):
    Bus.objects.filter(id=bus_id).delete()
    return redirect('mauribus_app:dashboard')

@never_cache
@login_required
def line_delete(request, line_id):
    Line.objects.filter(id=line_id).delete()
    return redirect('mauribus_app:dashboard')

@never_cache
@login_required
def trip_delete(request, trip_id):
    Trip.objects.filter(id=trip_id).delete()
    return redirect('mauribus_app:dashboard')

@never_cache
@login_required
def driver_delete(request, driver_id):
    Driver.objects.filter(id=driver_id).delete()
    return redirect('mauribus_app:dashboard')

@never_cache
@login_required
def user_delete(request, user_id):
    User.objects.filter(id=user_id).delete()
    return redirect('mauribus_app:dashboard')
   
# ---------- Bus ----------
@never_cache
@login_required(login_url='mauribus_app:login')
def bus_list(request):
    if request.method == "POST":
        bus_id = request.POST.get("bus_id")
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        status = request.POST.get("status")

        if bus_id:
            # Modifier
            bus = Bus.objects.get(id=bus_id)
            bus.name = name
            bus.capacity = capacity
            bus.status = status
            bus.save()
        else:
            # Ajouter
            Bus.objects.create(
                name=name,
                capacity=capacity,
                status=status
            )

        return redirect("mauribus_app:bus_list")

    return render(request, "admin/bus.html", {
        "buses": Bus.objects.all()
    })

@login_required(login_url='mauribus_app:login')
def bus_delete(request, bus_id):
    Bus.objects.filter(id=bus_id).delete()
    return redirect("mauribus_app:bus_list")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
import json

from .models import Line

# ---------- Line ----------

@never_cache
@login_required(login_url='mauribus_app:login')
def line_list(request):
    if request.method == "POST":
        line_id = request.POST.get("line_id")
        name = request.POST.get("name")
        start = request.POST.get("start")
        end = request.POST.get("end")

        if line_id:
            line = get_object_or_404(Line, id=line_id)
            line.name = name
            line.start = start
            line.end = end
            line.save()
        else:
            Line.objects.create(
                name=name,
                start=start,
                end=end
            )
        return redirect("mauribus_app:line_list")

    # Récupérer toutes les lignes
    lines_qs = Line.objects.all()

    # Transformer en liste de dicts pour JS (évite json_script direct)
    lines_list = list(lines_qs.values(
        'id', 'name', 'start', 'end', 'start_lat', 'start_lng', 'end_lat', 'end_lng'
    ))

    return render(request, "admin/lines.html", {
        "lines_list": lines_qs,
        "lines_json": json.dumps(lines_list)
    })


@never_cache
@login_required(login_url='mauribus_app:login')
def admin_set_line_points(request):
    """Réception des coordonnées via fetch JS"""
    if request.method == "POST":
        line_id = request.POST.get('line_id')
        start_lat = request.POST.get('start_lat')
        start_lng = request.POST.get('start_lng')
        end_lat = request.POST.get('end_lat')
        end_lng = request.POST.get('end_lng')

        try:
            line = Line.objects.get(id=line_id)
            line.start_lat = float(start_lat)
            line.start_lng = float(start_lng)
            line.end_lat = float(end_lat)
            line.end_lng = float(end_lng)
            line.save()
            return JsonResponse({'ok': True})
        except Line.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Ligne introuvable'})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})
    return JsonResponse({'ok': False, 'error': 'Méthode non autorisée'})


@login_required(login_url='mauribus_app:login')
def line_delete(request, line_id):
    Line.objects.filter(id=line_id).delete()
    return redirect("mauribus_app:line_list")

# ---------- Trip ----------
@never_cache
@login_required(login_url='mauribus_app:login')
def trip_list(request):
    if request.method == "POST":
        trip_id = request.POST.get("trip_id")
        bus_id = request.POST.get("bus")
        line_id = request.POST.get("line")
        date = request.POST.get("date")

        if trip_id:
            trip = Trip.objects.get(id=trip_id)
            trip.bus_id = bus_id
            trip.line_id = line_id
            trip.date = date
            trip.save()
        else:
            Trip.objects.create(
                bus_id=bus_id,
                line_id=line_id,
                date=date
            )

        return redirect("mauribus_app:trip_list")

    return render(request, "admin/trips.html", {
        "trips": Trip.objects.select_related("bus", "line"),
        "buses": Bus.objects.all(),
        "lines": Line.objects.all()
    })


@login_required(login_url='mauribus_app:login')
def trip_delete(request, trip_id):
    Trip.objects.filter(id=trip_id).delete()
    return redirect("mauribus_app:trip_list")

# ---------- Driver ----------
@never_cache
@login_required(login_url='mauribus_app:login')
def driver_list(request):
    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        if driver_id:
            driver = Driver.objects.get(id=driver_id)
            driver.name = name
            driver.phone = phone
            driver.save()
        else:
            Driver.objects.create(
                name=name,
                phone=phone
            )

        return redirect("mauribus_app:driver_list")

    return render(request, "admin/drivers.html", {
        "drivers": Driver.objects.all()
    })


@login_required(login_url='mauribus_app:login')
def driver_delete(request, driver_id):
    Driver.objects.filter(id=driver_id).delete()
    return redirect("mauribus_app:driver_list")

# ---------- Users ----------
@never_cache
@login_required(login_url='mauribus_app:login')
def user_list(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        email = request.POST.get("email")
        role = request.POST.get("role")

        if user_id:
            user = User.objects.get(id=user_id)
            user.email = email
            user.role = role
            user.save()

        return redirect("mauribus_app:user_list")

    return render(request, "admin/users.html", {
        "users": User.objects.all()
    })


@login_required(login_url='mauribus_app:login')
def user_delete(request, user_id):
    User.objects.filter(id=user_id).delete()
    return redirect("mauribus_app:user_list")



# ========== API ENDPOINTS FOR MOBILE APP ==========

def _get_user_from_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) != 2:
        return None
    scheme, token_key = parts
    if scheme.lower() not in ['bearer', 'token']:
        return None
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return None

@csrf_exempt
@require_http_methods(["POST"])
def api_auth_register(request):
    """Register a new citizen user"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        
        # Validation
        if not email or not password or not first_name or not last_name:
            return JsonResponse(
                {'error': 'Missing required fields'},
                status=400
            )
        
        if len(password) < 6:
            return JsonResponse(
                {'error': 'Password must be at least 6 characters'},
                status=400
            )
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'error': 'User with this email already exists'},
                status=400
            )
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_citizen=True
        )
        
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        return JsonResponse(
            {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'created_at': user.date_joined.isoformat()
                }
            },
            status=201
        )
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_auth_login(request):
    """Login a user and return token"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return JsonResponse(
                {'error': 'Email and password required'},
                status=400
            )
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if not user:
            return JsonResponse(
                {'error': 'Invalid email or password'},
                status=401
            )
        
        # Get token
        token, created = Token.objects.get_or_create(user=user)
        
        return JsonResponse({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'created_at': user.date_joined.isoformat()
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========== API ENDPOINTS FOR MOBILE APP ==========

@csrf_exempt
@require_http_methods(["GET"])
def api_lines(request):
    """Get all bus lines"""
    try:
        lines_data = []
        for line in Line.objects.all():
            lines_data.append({
                'id': line.id,
                'name': line.name,
                'description': '',
                'start_location': line.start,
                'end_location': line.end,
                'start_lat': line.start_lat,
                'start_lng': line.start_lng,
                'end_lat': line.end_lat,
                'end_lng': line.end_lng,
                'price': 0,
                'estimated_duration': 0,
            })
        return JsonResponse(lines_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_trips(request):
    """Get trips, optionally filtered by line"""
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        trips_query = Trip.objects.all().select_related('line', 'bus', 'bus__driver')
        
        # Filter by line_id if provided
        line_id = request.GET.get('line_id')
        if line_id:
            trips_query = trips_query.filter(line_id=line_id)
        
        trips_data = []
        status_map = {
            'scheduled': 'pending',
            'started': 'ongoing',
            'completed': 'completed',
            'cancelled': 'cancelled',
            'not_completed': 'cancelled',
        }

        for trip in trips_query:
            arrival_time = None
            if trip.date:
                arrival_time = (trip.date + timedelta(minutes=30)).isoformat()

            total_seats = trip.bus.capacity if trip.bus else 50
            available_seats = total_seats

            trips_data.append({
                'id': trip.id,
                'line_id': trip.line.id,
                'line_name': trip.line.name,
                'bus_id': trip.bus.id,
                'bus_name': trip.bus.name,
                'driver_name': trip.bus.driver.name if trip.bus and trip.bus.driver else 'Unknown',
                'departure_time': trip.date.isoformat() if trip.date else None,
                'arrival_time': arrival_time,
                'status': status_map.get(trip.status, 'pending'),
                'available_seats': available_seats,
                'total_seats': total_seats,
            })
        
        return JsonResponse(trips_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_user_profile(request):
    """Get current user profile (requires authentication)"""
    try:
        user = _get_user_from_token(request)
        if not user:
            return JsonResponse({'error': 'Not authenticated'}, status=401)

        return JsonResponse({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': getattr(user, 'phone', ''),
            'created_at': user.date_joined.isoformat()
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
