# 💻 Commandes Utiles - MauriBus

## 🚀 Démarrage du Serveur

### Lancer le serveur de développement
```bash
cd C:\Users\lalle\Desktop\MauriBus
python manage.py runserver
```

### Lancer sur un port spécifique
```bash
python manage.py runserver 8080
```

### Lancer sur 0.0.0.0 (accessible en réseau)
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🗄️ Base de Données

### Créer les migrations
```bash
python manage.py makemigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

### Créer un superuser (admin)
```bash
python manage.py createsuperuser
# Email: admin@example.com
# Password: admin123
```

### Réinitialiser la base de données
```bash
# ATTENTION: Supprime toutes les données!
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

---

## 🧪 Tests & Validation

### Vérifier qu'il n'y a pas d'erreurs Django
```bash
python manage.py check
```

### Lancer les tests
```bash
python manage.py test
python manage.py test mauribus_app
```

### Lancer les tests avec verbosité
```bash
python manage.py test --verbosity=2
```

---

## 🎨 Collecte des fichiers statiques

### Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### Collecter avec suppression
```bash
python manage.py collectstatic --clear --noinput
```

---

## 🐚 Django Shell

### Lancer la console Django
```bash
python manage.py shell
```

### Exemples de commandes dans le shell
```python
from mauribus_app.models import Bus, Driver, Trip, User, Message

# Voir tous les buses
buses = Bus.objects.all()
for bus in buses:
    print(f"{bus.name} - {bus.status}")

# Créer un trip
from datetime import datetime
trip = Trip.objects.create(
    bus=Bus.objects.first(),
    line=Line.objects.first(),
    status='ongoing',
    started_at=datetime.now()
)

# Voir tous les messages
messages = Message.objects.all()
for msg in messages:
    print(f"{msg.sender} → {msg.recipient}: {msg.content[:50]}")

# Créer un utilisateur
user = User.objects.create_user(
    email='test@example.com',
    password='test123',
    first_name='Test',
    last_name='User'
)

# Quitter la console
exit()
```

---

## 📁 Structure des Dossiers

```
C:\Users\lalle\Desktop\MauriBus\
├── manage.py
├── db.sqlite3
├── requirements.txt (optionnel)
│
├── mauribus_app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0004_trip_message.py
│   │   ├── 0005_line_coords.py
│   │   ├── 0006_driver_photo.py
│   │   └── __init__.py
│   └── __pycache__/
│
├── mauribus_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── users.html ✅ NEW
│   │   ├── drivers.html ✅ NEW
│   │   ├── trips.html ✅ NEW
│   │   ├── buses.html
│   │   ├── lines.html
│   │   ├── messages.html
│   │   └── login.html
│   │
│   ├── driver/
│   │   ├── dashboard.html ✅ UPDATED
│   │   ├── buses.html ✅ UPDATED
│   │   ├── messages.html ✅ NEW
│   │   ├── trips.html
│   │   ├── profile.html
│   │   ├── notifications.html
│   │   └── login.html
│   │
│   └── citizen/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/ (uploads)
│   └── driver_photos/
│
└── venv/ (environment)
```

---

## 🔍 Commandes de Recherche Utiles

### Trouver tous les fichiers `.html`
```bash
dir /s /b *.html
```

### Trouver tous les fichiers `.py`
```bash
dir /s /b *.py
```

### Chercher du texte dans tous les fichiers
```bash
findstr /r /s "driver_messages" *.py
```

---

## 🌐 URLs Importantes

### Local Development
```
Home Page: http://127.0.0.1:8000/
Admin Login: http://127.0.0.1:8000/login/
Driver Login: http://127.0.0.1:8000/driver/login/
Admin Dashboard: http://127.0.0.1:8000/
Driver Dashboard: http://127.0.0.1:8000/driver/dashboard/
```

### Admin Pages
```
Users: http://127.0.0.1:8000/users/
Drivers: http://127.0.0.1:8000/drivers/
Trips: http://127.0.0.1:8000/trips/
Buses: http://127.0.0.1:8000/buses/
Lines: http://127.0.0.1:8000/lines/
Messages: http://127.0.0.1:8000/admin/messages/
```

### Driver Pages
```
Dashboard: http://127.0.0.1:8000/driver/dashboard/
Buses: http://127.0.0.1:8000/driver/buses/
Messages: http://127.0.0.1:8000/driver/messages/
Trips: http://127.0.0.1:8000/driver/trips/
Profile: http://127.0.0.1:8000/driver/profile/
```

---

## 🔧 Configuration Settings.py

### Important
```python
# Line: DEBUG = True  (keep for development)
# Line: ALLOWED_HOSTS = ['*']  (for local dev)
# Line: MEDIA_URL = '/media/'
# Line: MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Vérifier la configuration
```bash
python manage.py diffsettings
```

---

## 🐛 Débogage

### Activer les logs Django
```python
# Dans settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Voir les requêtes SQL
```python
# Dans views.py
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    messages = Message.objects.filter(recipient=user)
    for query in context.captured_queries:
        print(query['sql'])
```

---

## 🚨 Troubleshooting

### Erreur: "Module not found"
```bash
# Vérifier l'environment
python -c "import django; print(django.VERSION)"

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur: "No such table"
```bash
# Appliquer les migrations
python manage.py migrate
```

### Erreur: "TemplateDoesNotExist"
```bash
# Vérifier le chemin du template
# Vérifier que TEMPLATES est configuré dans settings.py
python manage.py check
```

### Cache problems
```bash
# Vider le cache
python manage.py clear_cache

# Supprimer __pycache__
dir /s /b __pycache__ | del

# Redémarrer le serveur
# Ctrl+C puis python manage.py runserver
```

---

## 📦 Installation des Dépendances

### Créer requirements.txt
```bash
pip freeze > requirements.txt
```

### Installer depuis requirements.txt
```bash
pip install -r requirements.txt
```

### Dépendances principales
```
Django==4.2.0
Pillow==10.0.0
```

---

## 🚀 Production Checklist

- [ ] `DEBUG = False` dans settings.py
- [ ] `SECRET_KEY` est sécurisé (variable d'env)
- [ ] `ALLOWED_HOSTS` configuré correctement
- [ ] HTTPS forcé (`SECURE_SSL_REDIRECT = True`)
- [ ] `python manage.py check --deploy`
- [ ] Base de données en production (PostgreSQL)
- [ ] Fichiers statiques collectés
- [ ] Logs et monitoring configurés
- [ ] Backups automatiques DB
- [ ] Email d'erreurs configuré

---

## 📚 Ressources Utiles

### Django Docs
- https://docs.djangoproject.com/
- https://docs.djangoproject.com/en/4.2/

### Leaflet.js
- https://leafletjs.com/
- https://leafletjs.com/reference.html

### Font Awesome
- https://fontawesome.com/
- https://fontawesome.com/docs/web/setup/get-started

### Bootstrap/CSS
- https://getbootstrap.com/
- https://tailwindcss.com/

---

**Version: 2.1**
**Last Updated: 28 Jan 2026**
