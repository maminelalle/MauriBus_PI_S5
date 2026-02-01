from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ---------- User Manager ----------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L’email doit être défini')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_driver', False)
        extra_fields.setdefault('is_citizen', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


# ---------- User ----------
class User(AbstractUser):
    username = None  # on supprime le username
    email = models.EmailField(unique=True)
    is_driver = models.BooleanField(default=False)
    is_citizen = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # pour l’admin

    USERNAME_FIELD = 'email'       # l’identifiant unique devient l’email
    REQUIRED_FIELDS = []           # aucun autre champ obligatoire

    objects = CustomUserManager()  # on utilise le manager personnalisé

    def __str__(self):
        return self.email


# ---------- Bus ----------
class Bus(models.Model):
    STATUS_CHOICES = [
        ('service', 'En Service'),
        ('panne', 'En Panne'),
        ('maintenance', 'Maintenance'),
        ('garage', 'Au Garage'),
    ]
    
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True, related_name='buses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='service')
    lat = models.FloatField(default=14.7)
    lng = models.FloatField(default=-17.44)

    def __str__(self):
        return self.name


# ---------- Line ----------
class Line(models.Model):
    name = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    # Optional geo coordinates for map integration (lat, lng)
    start_lat = models.FloatField(null=True, blank=True)
    start_lng = models.FloatField(null=True, blank=True)
    end_lat = models.FloatField(null=True, blank=True)
    end_lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


# ---------- Trip ----------
class Trip(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('scheduled', 'Planifié'),
        ('started', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
        ('not_completed', 'Non terminé'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.line.name} - {self.bus.name}" + (f" - {self.date}" if self.date else "")


# Messages between admin and drivers
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='messages_received')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    broadcast = models.BooleanField(default=False)

    def __str__(self):
        to = 'All' if self.broadcast else (self.recipient.email if self.recipient else 'Admin')
        return f"Message from {self.sender.email} to {to} at {self.created_at}" 


# ---------- Driver ----------
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True)

    def __str__(self):
        return self.name
