# MauriBus Mobile App - Flutter

Application mobile citoyen (passagers) pour réserver et tracker les bus.

## Structure Projet

```
mauribus_mobile/
├── pubspec.yaml              # Dépendances Flutter
├── README.md                 # Guide de démarrage
├── lib/
│   ├── main.dart            # Point d'entrée app
│   ├── config/
│   │   ├── api_config.dart  # Configuration API Django
│   │   └── theme.dart       # Thème global
│   ├── models/
│   │   ├── line_model.dart
│   │   ├── trip_model.dart
│   │   ├── booking_model.dart
│   │   └── user_model.dart
│   ├── services/
│   │   ├── api_service.dart # Appels API Django
│   │   └── auth_service.dart
│   ├── screens/
│   │   ├── splash_screen.dart
│   │   ├── login_screen.dart
│   │   ├── home_screen.dart
│   │   ├── lines_screen.dart
│   │   ├── trips_screen.dart
│   │   ├── booking_screen.dart
│   │   ├── profile_screen.dart
│   │   └── history_screen.dart
│   ├── widgets/
│   │   ├── line_card.dart
│   │   ├── trip_card.dart
│   │   ├── bottom_nav.dart
│   │   └── custom_app_bar.dart
│   └── providers/
│       ├── auth_provider.dart
│       ├── lines_provider.dart
│       └── trips_provider.dart
│
├── android/                  # Configuration Android
├── ios/                      # Configuration iOS
└── assets/                   # Images, icons, etc
    └── images/
```

## Fonctionnalités

✅ Authentification (email/password)
✅ Consulter les lignes disponibles
✅ Voir les trajets en temps réel
✅ Réserver un ticket
✅ Historique des réservations
✅ Profil utilisateur
✅ Notifications push (optionnel)

## Dépendances Principales

- `provider` - State management
- `http` - API calls
- `shared_preferences` - Local storage
- `intl` - Localisation
- `google_maps_flutter` - Carte (optionnel)
- `flutter_local_notifications` - Notifications
