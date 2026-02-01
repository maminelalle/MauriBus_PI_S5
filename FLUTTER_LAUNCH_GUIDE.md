╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                   🚀 GUIDE DE LANCEMENT - MAURIBUS APP 🚀                  ║
║                                                                              ║
║                         Application Mobile Flutter                          ║
║                        Interface Citoyens (Passagers)                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════════════
 ÉTAPE 1: INSTALLER FLUTTER
═══════════════════════════════════════════════════════════════════════════════════

1. Télécharger Flutter:
   → https://flutter.dev/docs/get-started/install

2. Extraire le fichier dans un dossier (ex: C:\flutter)

3. Ajouter Flutter au PATH:
   a. Ouvrir Paramètres → Variables d'environnement
   b. Créer une nouvelle variable: FLUTTER_HOME = C:\flutter
   c. Ajouter au PATH: %FLUTTER_HOME%\bin

4. Vérifier l'installation:
   ```bash
   flutter doctor
   ```
   ✓ Doit afficher: "No issues found!"


═══════════════════════════════════════════════════════════════════════════════════
 ÉTAPE 2: PRÉPARER LE PROJET
═══════════════════════════════════════════════════════════════════════════════════

1. Ouvrir PowerShell dans le dossier du projet:
   ```
   C:\Users\lalle\Desktop\MauriBus\mauribus_mobile
   ```

2. Installer les dépendances:
   ```bash
   flutter pub get
   ```
   Cela télécharge tous les packages (provider, http, shared_preferences, etc.)


═══════════════════════════════════════════════════════════════════════════════════
 ÉTAPE 3: CONFIGURER L'API (IMPORTANT!)
═══════════════════════════════════════════════════════════════════════════════════

1. Éditer: lib/config/api_config.dart

2. Configurer l'URL du serveur Django:
   ```dart
   static const String baseUrl = 'http://192.168.1.XX:8000';
   ```
   
   ⚠️ IMPORTANT:
   - Sur émulateur Android: utiliser 10.0.2.2:8000 au lieu de localhost
   - Sur émulateur iOS: utiliser localhost:8000
   - Sur appareil réel: utiliser l'IP locale (ex: 192.168.1.100:8000)

3. Vérifier que le serveur Django tourne:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```


═══════════════════════════════════════════════════════════════════════════════════
 ÉTAPE 4: LANCER L'APPLICATION
═══════════════════════════════════════════════════════════════════════════════════

### Option A: SUR ÉMULATEUR ANDROID

1. Ouvrir Android Studio
2. Créer/démarrer un émulateur Android
3. Dans le dossier mauribus_mobile:
   ```bash
   flutter run
   ```

### Option B: SUR ÉMULATEUR iOS (macOS uniquement)

1. Démarrer l'émulateur iOS:
   ```bash
   open -a Simulator
   ```
2. Lancer l'app:
   ```bash
   flutter run
   ```

### Option C: SUR APPAREIL RÉEL ANDROID

1. Connecter un téléphone Android en USB
2. Activer le "Débogage USB" dans Paramètres → Options pour développeurs
3. Vérifier que l'appareil est reconnu:
   ```bash
   flutter devices
   ```
4. Lancer l'app:
   ```bash
   flutter run
   ```


═══════════════════════════════════════════════════════════════════════════════════
 ÉCRANS INCLUS DANS L'APP
═══════════════════════════════════════════════════════════════════════════════════

✅ SplashScreen
   → Écran de démarrage de 2 secondes
   → Transition vers LoginScreen

✅ LoginScreen
   → Email + Password
   → Inscription (lien)
   → Gestion des erreurs

✅ HomeScreen (Principal)
   → Liste des lignes de bus
   → Recherche
   → Pull-to-refresh
   → Navigation vers TripsScreen

✅ TripsScreen
   → Trajets filtrés par ligne
   → Filtres par statut
   → Affichage places disponibles
   → Navigation vers BookingScreen

✅ BookingScreen
   → Sélection nombre de places
   → Affichage du prix
   → Confirmation avec code ticket
   → Dialog de succès

✅ HistoryScreen
   → Historique de toutes les réservations
   → Filtrage par statut
   → Affichage du code ticket
   → Options de partage et QR code

✅ ProfileScreen
   → Informations utilisateur
   → Statistiques (trajets, économies, points)
   → Préférences
   → Bouton déconnexion


═══════════════════════════════════════════════════════════════════════════════════
 DESIGN ET COMPONENTS
═══════════════════════════════════════════════════════════════════════════════════

🎨 Thème Material Design 3:
   - Couleur primaire: Bleu (#2563eb)
   - Couleur secondaire: Violet (#667eea)
   - Couleur succès: Vert (#10b981)
   - Couleur warning: Orange (#f59e0b)
   - Couleur error: Rouge (#ef4444)

📱 Components réutilisables:
   ✓ LineCard: Affichage d'une ligne
   ✓ TripCard: Affichage d'un trajet avec statut
   ✓ CustomAppBar: Barre d'app personnalisée
   ✓ BookingButton: Bouton de réservation avec loading
   ✓ EmptyState: Écran vide avec message
   ✓ CustomBottomNavBar: Navigation inférieure

🔄 Navigation:
   ✓ Splash → Login (auto après 2s)
   ✓ Login → Home (après succès)
   ✓ Home → Trips (par ligne)
   ✓ Trips → Booking (par trajet)
   ✓ Navigation inférieure (Home, Mes trajets, Historique, Profil)


═══════════════════════════════════════════════════════════════════════════════════
 STRUCTURE DU PROJET
═══════════════════════════════════════════════════════════════════════════════════

mauribus_mobile/
├── lib/
│   ├── main.dart                          ← Point d'entrée
│   ├── config/
│   │   ├── api_config.dart               ← Configuration API
│   │   └── theme.dart                    ← Thème global
│   ├── models/
│   │   └── models.dart                   ← Modèles (Line, Trip, Booking, User)
│   ├── services/
│   │   └── api_service.dart              ← Service HTTP (singleton)
│   ├── providers/
│   │   ├── auth_provider.dart            ← Auth state
│   │   ├── lines_provider.dart           ← Lines state
│   │   ├── trips_provider.dart           ← Trips state
│   │   └── booking_provider.dart         ← Bookings state
│   ├── screens/
│   │   ├── splash_screen.dart
│   │   ├── login_screen.dart
│   │   ├── home_screen.dart
│   │   ├── trips_screen.dart
│   │   ├── booking_screen.dart
│   │   ├── profile_screen.dart
│   │   └── history_screen.dart
│   └── widgets/
│       ├── custom_app_bar.dart
│       ├── line_card.dart
│       ├── trip_card.dart
│       ├── booking_button.dart
│       ├── empty_state.dart
│       └── custom_bottom_nav_bar.dart
│
├── pubspec.yaml                          ← Dépendances
├── android/                              ← Code Android (auto-généré)
├── ios/                                  ← Code iOS (auto-généré)
└── assets/                               ← Images et ressources


═══════════════════════════════════════════════════════════════════════════════════
 DÉPENDANCES
═══════════════════════════════════════════════════════════════════════════════════

flutter_lints: ^2.0.0          ← Linting
provider: ^6.0.0               ← State management
http: ^1.1.0                   ← HTTP client
dio: ^5.3.0                    ← HTTP avancé (optionnel)
shared_preferences: ^2.2.0     ← Stockage local (tokens)
google_fonts: ^6.1.0           ← Polices Google
intl: ^0.18.0                  ← Internationalisation
google_maps_flutter: ^2.5.0    ← Maps (optionnel)
flutter_local_notifications:   ← Notifications


═══════════════════════════════════════════════════════════════════════════════════
 DÉPANNAGE
═══════════════════════════════════════════════════════════════════════════════════

❌ Problème: "flutter: Le terme n'est pas reconnu"
✅ Solution: Ajouter Flutter au PATH (voir ÉTAPE 1)

❌ Problème: "Erreur de connexion à l'API"
✅ Solution: Vérifier que:
   1. Serveur Django tourne (python manage.py runserver)
   2. URL API_config.dart correcte
   3. CORS activé dans Django settings.py

❌ Problème: Erreurs build Android
✅ Solution:
   ```bash
   flutter clean
   flutter pub get
   flutter run
   ```

❌ Problème: App se ferme au lancement
✅ Solution:
   1. Vérifier les logs: flutter run -v
   2. S'assurer que ApiService.init() est appelé
   3. Vérifier la configuration API


═══════════════════════════════════════════════════════════════════════════════════
 PROCHAINES ÉTAPES
═══════════════════════════════════════════════════════════════════════════════════

1. ✅ Installer Flutter SDK
2. ✅ Lancer l'app sur émulateur/appareil
3. ⏳ Tester l'authentification (login/register)
4. ⏳ Vérifier les appels API
5. ⏳ Tester les réservations
6. ⏳ Personnaliser à vos besoins

Si vous avez besoin d'aide:
→ Consulter les logs: flutter run -v
→ Vérifier Flutter: flutter doctor
→ Voir les erreurs: flutter build apk


═══════════════════════════════════════════════════════════════════════════════════
 COMMANDES UTILES
═══════════════════════════════════════════════════════════════════════════════════

# Installer les dépendances
flutter pub get

# Lancer l'app
flutter run

# Lancer avec logs détaillés
flutter run -v

# Build APK
flutter build apk

# Build APK split (plus petit)
flutter build apk --split-per-abi

# Nettoyer
flutter clean

# Voir les appareils disponibles
flutter devices

# Vérifier la santé
flutter doctor

# Formater le code
dart format lib/

# Analyser le code
dart analyze


═══════════════════════════════════════════════════════════════════════════════════
 CONTACT & SUPPORT
═══════════════════════════════════════════════════════════════════════════════════

Documentation Flutter: https://flutter.dev/docs
Provider Package: https://pub.dev/packages/provider
Material Design 3: https://m3.material.io/

Bonne chance! 🎉

═══════════════════════════════════════════════════════════════════════════════════
