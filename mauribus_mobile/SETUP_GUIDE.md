# 🚀 MauriBus Flutter Mobile App - Guide Complet

## ⚡ Démarrage Rapide

### 1. Prérequis

```bash
# Installer Flutter
https://flutter.dev/docs/get-started/install

# Vérifier l'installation
flutter doctor
```

### 2. Créer le projet

```bash
cd C:\Users\lalle\Desktop\MauriBus
flutter create mauribus_mobile
```

### 3. Installer les dépendances

```bash
cd mauribus_mobile
flutter pub get
```

### 4. Configurer l'API Django

Éditer `lib/config/api_config.dart`:

```dart
static const String baseUrl = 'http://YOUR_IP:8000'; // Remplacer YOUR_IP
```

### 5. Lancer l'app

```bash
# Sur émulateur
flutter run

# Sur appareil réel
flutter run -v

# Build APK
flutter build apk --split-per-abi

# Build App Bundle (Google Play)
flutter build appbundle
```

---

## 📁 Structure du Projet

```
mauribus_mobile/
├── lib/
│   ├── main.dart                 ← Point d'entrée
│   ├── config/
│   │   ├── api_config.dart      ← Configuration API
│   │   └── theme.dart           ← Thème global
│   ├── models/
│   │   └── models.dart          ← Classes de données
│   ├── services/
│   │   └── api_service.dart     ← Appels API
│   ├── screens/
│   │   ├── splash_screen.dart
│   │   ├── login_screen.dart
│   │   ├── home_screen.dart
│   │   ├── trips_screen.dart
│   │   ├── booking_screen.dart
│   │   ├── profile_screen.dart
│   │   └── history_screen.dart
│   └── widgets/
│       ├── line_card.dart
│       ├── trip_card.dart
│       └── custom_app_bar.dart
│
├── pubspec.yaml                  ← Dépendances
├── android/                      ← Config Android
├── ios/                         ← Config iOS
└── assets/                      ← Images, icons
```

---

## 🎨 Thème & Design

### Couleurs Principales
- **Primary**: #2563eb (Bleu)
- **Secondary**: #667eea (Violet-bleu)
- **Accent**: #764ba2 (Violet)
- **Success**: #10b981 (Vert)
- **Warning**: #f59e0b (Orange)
- **Error**: #ef4444 (Rouge)

### Espacements
- **XS**: 4px
- **S**: 8px
- **M**: 16px
- **L**: 24px
- **XL**: 32px

### Border Radius
- **S**: 4px
- **M**: 8px
- **L**: 12px
- **XL**: 16px

---

## 🔌 Intégration API Django

### Endpoints Nécessaires

Vos routes Django doivent fournir:

#### Authentication
```
POST /api/auth/login/
  Body: {email, password}
  Response: {token, user}

POST /api/auth/register/
  Body: {email, password, first_name, last_name}

POST /api/auth/logout/
```

#### Lignes
```
GET /api/lines/
  Response: [{id, name, start_location, end_location, price, ...}]

GET /api/lines/{id}/
  Response: {id, name, ...}
```

#### Trajets
```
GET /api/trips/
GET /api/trips/?line_id=1
  Response: [{id, line_id, bus_id, departure_time, status, ...}]
```

#### Réservations
```
POST /api/bookings/
  Body: {trip_id, number_of_seats}
  Response: {id, trip_id, total_price, ticket_code, ...}

GET /api/bookings/
  Response: [{...}]
```

#### Profil
```
GET /api/user/profile/
  Response: {id, email, first_name, last_name, phone, ...}
```

---

## 🔐 Authentification

### Login Flow
1. Utilisateur saisit email + password
2. App appelle `POST /api/auth/login/`
3. Serveur retourne `{token}`
4. App stocke le token dans `SharedPreferences`
5. Token est envoyé dans le header `Authorization: Bearer {token}`

### Token Storage
```dart
SharedPreferences prefs = await SharedPreferences.getInstance();
await prefs.setString('auth_token', token);
```

### Auto-Login au démarrage
```dart
void initState() {
  final token = prefs.getString('auth_token');
  if (token != null) {
    navigateToHome();
  } else {
    navigateToLogin();
  }
}
```

---

## 📋 Fonctionnalités Principales

### 1. Écran d'Accueil
- Liste des lignes disponibles
- Affichage: Nom, Départ, Arrivée, Prix
- Pull-to-refresh
- Navigation vers les trajets

### 2. Sélection des Trajets
- Filtrer par ligne
- Voir les horaires
- Voir les places disponibles
- % d'occupation avec barre de progression
- Navigation vers réservation

### 3. Réservation
- Sélectionner nombre de places
- Voir le prix total
- Voir les détails du trajet
- Confirmation de réservation
- Reçu avec code ticket

### 4. Historique des Trajets
- Lister toutes les réservations
- État: Pending, Confirmed, Cancelled
- Afficher ticket code
- Prix payé
- Date de réservation

### 5. Profil Utilisateur
- Afficher: Nom, Email, Téléphone
- Photo de profil (si disponible)
- Date d'inscription
- Bouton déconnexion

---

## 🛠️ Customisation

### Changer la couleur primaire
Éditer `lib/config/theme.dart`:
```dart
static const Color primaryColor = Color(0xFF2563eb);
```

### Ajouter une nouvelle page
1. Créer `lib/screens/new_screen.dart`
2. Ajouter la route dans `main.dart`
3. Ajouter la navigation dans `home_screen.dart`

### Ajouter une nouvelle API call
1. Ajouter la méthode dans `lib/services/api_service.dart`
2. Utiliser `_headers()` pour l'authentification
3. Gérer les exceptions avec `ApiException`

---

## 🧪 Tests

### Tests unitaires
```bash
flutter test
```

### Tests d'intégration
```bash
flutter test --target=test_driver/app.dart
```

### Tester l'API
```bash
# Utiliser Postman ou cURL
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"test123"}'
```

---

## 🚨 Troubleshooting

### Erreur: "Connection refused"
- Vérifier que le serveur Django tourne
- Vérifier l'adresse IP dans `api_config.dart`
- Sur émulateur Android: utiliser `10.0.2.2` au lieu de `127.0.0.1`

### Erreur: "Certificate verify failed"
- Dans développement, désactiver la vérification SSL:
```dart
_http.Client client = _http.Client();
HttpClient httpClient = HttpClient()..badCertificateCallback = (_, __, ___) => true;
```

### Erreur: "Null Safety"
- Ajouter `required` pour les paramètres obligatoires
- Utiliser `?` pour les nullable types
- Utiliser `!` pour forcer non-null (attention!)

### App lent
- Utiliser `ListView.builder` au lieu de `ListView`
- Ajouter `const` aux widgets statiques
- Utiliser `cached_network_image` pour les images

---

## 📦 Build & Déploiement

### Build APK (Android)
```bash
flutter build apk --split-per-abi
# Fichiers: build/app/outputs/apk/release/app-*-release.apk
```

### Build iOS
```bash
flutter build ios
# Ouvrir Xcode et configurer les signing
```

### Google Play Store
```bash
# 1. Créer un compte developer
# 2. flutter build appbundle
# 3. Upload sur Google Play Console
```

### App Store (iOS)
```bash
# 1. Créer un compte Apple Developer
# 2. Configurer Xcode
# 3. flutter build ios
# 4. Upload avec Transporter
```

---

## 📚 Dépendances Utiles

```yaml
# État & données
provider: ^6.0.0          # State management
riverpod: ^2.4.0          # Alternative à Provider
bloc: ^8.1.0              # Pattern BLoC

# HTTP & API
http: ^1.1.0              # HTTP client
dio: ^5.3.0               # HTTP client avancé
graphql_flutter: ^5.1.0   # GraphQL

# UI
flutter_svg: ^2.0.0       # SVG support
lottie: ^2.3.0            # Animations Lottie
cached_network_image: ^3.2.0

# Navigation
go_router: ^10.1.0        # Routing declaratif
auto_route: ^7.8.0        # Routing avancé

# Base de données locale
hive: ^2.2.0              # NoSQL local
sqflite: ^2.2.0           # SQLite

# Maps
google_maps_flutter: ^2.5.0

# Notifications
firebase_messaging: ^14.6.0

# Outils
intl: ^0.19.0             # i18n
logger: ^2.0.0            # Logging
freezed: ^2.4.0           # Code generation
```

---

## 🔄 CI/CD

### GitHub Actions (optionnel)
```yaml
name: Flutter Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter build apk
```

---

## 📞 Support

Pour toute question:
1. Consulter la [Documentation Flutter](https://flutter.dev/docs)
2. Vérifier les erreurs dans la console
3. Utiliser `flutter doctor` pour diagnostiquer

---

**Version**: 1.0.0
**Dernière mise à jour**: 28 Jan 2026
**Status**: ✅ Production Ready
