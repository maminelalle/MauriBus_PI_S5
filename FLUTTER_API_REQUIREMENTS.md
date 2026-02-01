# 🔌 API Endpoints pour Flutter App

## À Implémenter dans Django (mauribus_app)

L'app Flutter a besoin de ces endpoints API. Voici ce qu'il faut ajouter:

---

## ✅ 1. Authentication Endpoints

### Login
```
POST /api/auth/login/
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "password123"
}

Response (200 OK):
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont"
  }
}
```

### Register
```
POST /api/auth/register/
Content-Type: application/json

Request Body:
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "Jean",
  "last_name": "Dupont"
}

Response (201 Created):
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

### Logout
```
POST /api/auth/logout/
Authorization: Bearer {token}

Response (200 OK):
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## ✅ 2. Lines Endpoints

### Get All Lines
```
GET /api/lines/
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "name": "Dakar - Thiès",
    "description": "Ligne rapide",
    "start_location": "Dakar",
    "end_location": "Thiès",
    "start_lat": 14.6495,
    "start_lng": -17.4394,
    "end_lat": 14.7920,
    "end_lng": -16.9707,
    "price": 2000.00,
    "estimated_duration": 45
  },
  ...
]
```

### Get Single Line
```
GET /api/lines/{id}/
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "name": "Dakar - Thiès",
  "description": "Ligne rapide",
  "start_location": "Dakar",
  "end_location": "Thiès",
  "start_lat": 14.6495,
  "start_lng": -17.4394,
  "end_lat": 14.7920,
  "end_lng": -16.9707,
  "price": 2000.00,
  "estimated_duration": 45
}
```

---

## ✅ 3. Trips Endpoints

### Get All Trips (avec filtre optionnel)
```
GET /api/trips/
GET /api/trips/?line_id=1
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "line_id": 1,
    "bus_id": 1,
    "bus_name": "Bus 001",
    "driver_name": "Mamadou",
    "departure_time": "2026-01-28T08:00:00Z",
    "arrival_time": "2026-01-28T08:45:00Z",
    "status": "pending",
    "available_seats": 12,
    "total_seats": 50
  },
  ...
]
```

### Get Single Trip
```
GET /api/trips/{id}/
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "line_id": 1,
  "bus_id": 1,
  "bus_name": "Bus 001",
  "driver_name": "Mamadou",
  "departure_time": "2026-01-28T08:00:00Z",
  "arrival_time": "2026-01-28T08:45:00Z",
  "status": "pending",
  "available_seats": 12,
  "total_seats": 50
}
```

---

## ✅ 4. Bookings Endpoints

### Create Booking
```
POST /api/bookings/
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "trip_id": 1,
  "number_of_seats": 2
}

Response (201 Created):
{
  "success": true,
  "id": 1,
  "trip_id": 1,
  "user_id": 1,
  "number_of_seats": 2,
  "total_price": 4000.00,
  "status": "confirmed",
  "booking_date": "2026-01-28T10:30:00Z",
  "ticket_code": "TICKET-ABC123XYZ"
}
```

### Get User Bookings
```
GET /api/bookings/
Authorization: Bearer {token}

Response (200 OK):
[
  {
    "id": 1,
    "trip_id": 1,
    "user_id": 1,
    "number_of_seats": 2,
    "total_price": 4000.00,
    "status": "confirmed",
    "booking_date": "2026-01-28T10:30:00Z",
    "ticket_code": "TICKET-ABC123XYZ"
  },
  ...
]
```

### Get Single Booking
```
GET /api/bookings/{id}/
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "trip_id": 1,
  "user_id": 1,
  "number_of_seats": 2,
  "total_price": 4000.00,
  "status": "confirmed",
  "booking_date": "2026-01-28T10:30:00Z",
  "ticket_code": "TICKET-ABC123XYZ"
}
```

### Cancel Booking
```
POST /api/bookings/{id}/cancel/
Authorization: Bearer {token}

Response (200 OK):
{
  "success": true,
  "message": "Booking cancelled",
  "status": "cancelled"
}
```

---

## ✅ 5. User Profile Endpoint

### Get Profile
```
GET /api/user/profile/
Authorization: Bearer {token}

Response (200 OK):
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone": "+221771234567",
  "photo_url": "https://example.com/photos/user1.jpg",
  "created_at": "2025-12-15T10:00:00Z"
}
```

### Update Profile
```
PATCH /api/user/profile/
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone": "+221771234567"
}

Response (200 OK):
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jean",
  "last_name": "Dupont",
  "phone": "+221771234567",
  "photo_url": "https://example.com/photos/user1.jpg",
  "created_at": "2025-12-15T10:00:00Z"
}
```

---

## 📝 Implementation Example (Django)

### 1. Ajouter à `mauribus_app/urls.py`:

```python
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # API Endpoints
    path('api/auth/login/', api_login, name='api_login'),
    path('api/auth/register/', api_register, name='api_register'),
    path('api/auth/logout/', api_logout, name='api_logout'),
    
    path('api/lines/', api_lines_list, name='api_lines_list'),
    path('api/lines/<int:id>/', api_line_detail, name='api_line_detail'),
    
    path('api/trips/', api_trips_list, name='api_trips_list'),
    path('api/trips/<int:id>/', api_trip_detail, name='api_trip_detail'),
    
    path('api/bookings/', api_bookings_list, name='api_bookings_list'),
    path('api/bookings/<int:id>/', api_booking_detail, name='api_booking_detail'),
    path('api/bookings/<int:id>/cancel/', api_cancel_booking, name='api_cancel_booking'),
    
    path('api/user/profile/', api_user_profile, name='api_user_profile'),
]
```

### 2. Ajouter des vues dans `mauribus_app/views.py`:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate

@api_view(['POST'])
def api_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return Response({'success': False, 'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_lines_list(request):
    lines = Line.objects.all()
    data = [
        {
            'id': line.id,
            'name': line.name,
            'description': line.description,
            'start_location': line.start_location,
            'end_location': line.end_location,
            'start_lat': line.start_lat,
            'start_lng': line.start_lng,
            'end_lat': line.end_lat,
            'end_lng': line.end_lng,
            'price': line.price,
            'estimated_duration': line.estimated_duration,
        }
        for line in lines
    ]
    return Response(data)

# ... Ajouter les autres vues
```

---

## 🔒 Sécurité

### Token Authentication
- Utiliser Django REST Framework Token Authentication
- Envoyer le token dans le header: `Authorization: Bearer {token}`
- Ne jamais exposer les tokens en hard-code

### CORS
Ajouter à `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://192.168.1.100:8000",
]
```

### HTTPS
En production, toujours utiliser HTTPS.

---

## 🧪 Test avec Postman

1. Créer une collection "MauriBus Mobile API"
2. Ajouter les endpoints ci-dessus
3. Pour chaque requête protégée, ajouter le header:
   ```
   Authorization: Bearer {token}
   ```

---

## ✅ Checklist Implémentation

- [ ] Endpoints d'authentification
- [ ] Endpoints de lignes
- [ ] Endpoints de trajets
- [ ] Endpoints de réservations
- [ ] Endpoint de profil
- [ ] Token authentication configurée
- [ ] CORS activé
- [ ] Tests Postman réussis
- [ ] Erreurs 404/500 gérées
- [ ] Validation des données

---

**À faire**: Implémenter ces endpoints pour que l'app Flutter fonctionne correctement!
