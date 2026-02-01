# 📖 Guide d'Accès - MauriBus v2.1

## 🔐 Authentification

### Compte Admin
```
URL: http://127.0.0.1:8000/login/
Email: admin@example.com
Mot de passe: admin123
Rôle: Administrateur (is_staff=True)
```

### Compte Driver
```
URL: http://127.0.0.1:8000/driver/login/
Email: driver@example.com (ou autre driver existant)
Mot de passe: driver123
Rôle: Chauffeur
```

---

## 📱 Interface Admin

### 🏠 Page Accueil (Dashboard)
```
URL: http://127.0.0.1:8000/
Fonctionnalités:
├─ Statistiques globales (buses, trajets, drivers)
├─ Carte interactive Leaflet
├─ Messagerie rapide (card gradient)
├─ Tables: Bus, Lignes, Trajets
└─ Navigation vers toutes les sections
```

### 🚌 Gestion des Autobus
```
URL: http://127.0.0.1:8000/buses/
Template: templates/admin/bus.html
├─ Liste tous les buses
├─ Statut (En Service, En Panne, Maintenance, Garage)
├─ Affiche: Capacité, Couleur, Brand, Coordonnées GPS
└─ Carte interactive pour visualiser les positions
```

### 🚦 Gestion des Lignes
```
URL: http://127.0.0.1:8000/lines/
Template: templates/admin/lines.html
├─ Liste toutes les lignes
├─ Points départ/arrivée sur carte interactive
├─ Clic sur "Sur la Carte" pour éditer les coordonnées
├─ Polylines reliant les deux points
└─ Édition interactive des points GPS
```

### ✈️ Gestion des Trajets [NOUVEAU]
```
URL: http://127.0.0.1:8000/trips/
Template: templates/admin/trips.html ✅ NOUVEAU
├─ Tableau complet de tous les trajets
├─ Colonnes: Bus, Ligne, Chauffeur, Heure Départ, Heure Arrivée, Statut
├─ Status badges: En attente, En cours, Complété, Annulé
├─ Icônes Font Awesome
└─ Responsive design
```

### 👔 Gestion des Chauffeurs [NOUVEAU]
```
URL: http://127.0.0.1:8000/drivers/
Template: templates/admin/drivers.html ✅ NOUVEAU
├─ Tableau de tous les chauffeurs
├─ Colonnes: Nom, Téléphone, ID, Email, Date embauche, Statut
├─ Avatar avec première lettre du nom
├─ Status actif/inactif
└─ Informations de contact complètes
```

### 👥 Gestion des Utilisateurs [NOUVEAU]
```
URL: http://127.0.0.1:8000/users/
Template: templates/admin/users.html ✅ NOUVEAU
├─ Tableau de tous les utilisateurs
├─ Colonnes: Nom, Email, Rôle, Date inscription, Actif?
├─ Badges: Admin (bleu), Utilisateur (vert)
├─ Filtre actif/inactif
└─ Infos de création de compte
```

### 💬 Messagerie Admin
```
URL: http://127.0.0.1:8000/admin/messages/
Template: templates/admin/messages.html
├─ Envoi de messages aux drivers
├─ Options: Diffusion broadcast OU Driver spécifique
├─ Sélection du driver/trajet optionnel
├─ Vue de la conversation (tous les messages envoyés)
├─ Horodatage et métadonnées
└─ Markups badges (broadcast, trip)
```

---

## 👨‍💼 Interface Driver (Chauffeur)

### 🏢 Dashboard du Chauffeur
```
URL: http://127.0.0.1:8000/driver/dashboard/
Template: templates/driver/dashboard.html ✅ AMÉLIORÉ
Fonctionnalités:
├─ Statistiques: Trajets aujourd'hui, Assignés, Complétés, En cours
├─ Stats cards avec icônes et couleurs distinctes
├─ Carte Leaflet avec itinéraires de trajets
├─ Tableau: Trajets récents
├─ Card Messagerie (gradient, cliquable)
├─ Actions rapides (Trajets, Bus, Profil)
└─ Navigation complète
```

### 🚗 Mes Bus
```
URL: http://127.0.0.1:8000/driver/buses/
Template: templates/driver/buses.html ✅ REDESIGNÉ
Design:
├─ Grille responsive de cartes
├─ Carte par bus contient:
│  ├─ Nom du bus + ID
│  ├─ Status badge: En Service (🟢) | En Panne (🔴) | Maintenance (🟠) | Garage (🟣)
│  ├─ Capacité en places
│  ├─ Couleur & Marque
│  ├─ Position GPS (Latitude/Longitude)
│  └─ Boutons: Signaler problème, Détails
├─ Hover effect: Élévation (-4px)
├─ Border-left: 4px bleu (#3b82f6)
└─ Empty state si aucun bus
```

### 📍 Mes Trajets
```
URL: http://127.0.0.1:8000/driver/trips/
Template: templates/driver/trips.html
Fonctionnalités:
├─ Tableau des trajets assignés
├─ Colonnes: Date, Ligne, Bus, Heure Départ, Heure Arrivée, Statut
├─ Carte Leaflet montrant les itinéraires
├─ Status: Planifié (bleu), En cours (jaune), Terminé (vert)
├─ Popups sur la carte pour plus d'infos
└─ Responsive design
```

### 💬 Messagerie Driver [NOUVEAU]
```
URL: http://127.0.0.1:8000/driver/messages/
Template: templates/driver/messages.html ✅ NOUVEAU
Fonctionnalités:
├─ Vue tous les messages de l'admin
├─ Chaque message affiche:
│  ├─ Expéditeur: "Administration"
│  ├─ Horodatage (d/m/Y H:i)
│  ├─ Contenu du message
│  ├─ Badges:
│  │  ├─ Diffusion (jaune) si broadcast
│  │  ├─ Non lu (bleu) si not is_read
│  │  └─ Trajet (vert) si lié à un trajet
│  └─ Métadonnées: Bus, Ligne, Statut trajet
├─ Empty state élégant si aucun message
└─ Bouton "Retour au Tableau de Bord"
```

### 👤 Mon Profil
```
URL: http://127.0.0.1:8000/driver/profile/
Template: templates/driver/profile.html
Fonctionnalités:
├─ Avatar: Photo uploadée OU Icône user par défaut
├─ Section Informations de Contact
│  ├─ Téléphone
│  └─ Email
├─ Section Informations Professionnelles
│  ├─ ID Chauffeur
│  └─ Date d'engagement
├─ Profil en LECTURE SEULE (pas de modification)
└─ Bouton retour au tableau de bord
```

---

## 🔗 Carte de Navigation

### Depuis Admin Dashboard
```
[Home] → [Buses] → [Lines] → [Trips] → [Drivers] → [Users] → [Messages] → [Logout]
```

### Depuis Driver Dashboard
```
[Dashboard] → [Mes Trajets] → [Mes Bus] → [Messages] → [Mon Profil] → [Déconnexion]
```

---

## 🧪 Test Checklist

### Admin Interface
- [ ] `/` (dashboard) charge correctement
- [ ] `/buses/` affiche tableau + carte
- [ ] `/lines/` affiche tableau + interactive map
- [ ] `/trips/` affiche tableau ✅ NOUVEAU
- [ ] `/drivers/` affiche tableau ✅ NOUVEAU
- [ ] `/users/` affiche tableau ✅ NOUVEAU
- [ ] `/admin/messages/` permet envoi messages
- [ ] Tous les liens de nav fonctionnent

### Driver Interface
- [ ] `/driver/dashboard/` affiche stats + carte
- [ ] Lien "Messages" dans nav ✅ NOUVEAU
- [ ] `/driver/buses/` affiche grille cartes ✅ REDESIGNÉ
- [ ] `/driver/messages/` affiche messagerie ✅ NOUVEAU
- [ ] `/driver/trips/` affiche trajets
- [ ] `/driver/profile/` affiche profil
- [ ] Messages reçus s'affichent dans `/driver/messages/`
- [ ] Tous les liens de nav fonctionnent

### Responsive Design
- [ ] Interfaces responsive sur mobile (< 768px)
- [ ] Grilles cartes adaptatives
- [ ] Menus mobiles fonctionnent
- [ ] Tables lisibles sur petit écran

---

## 📊 Données de Test

### Créer un Trajet de Test
```python
# Dans Django shell:
from mauribus_app.models import Trip, Bus, Line
from datetime import datetime

trip = Trip.objects.create(
    bus=Bus.objects.first(),
    line=Line.objects.first(),
    status='ongoing',
    started_at=datetime.now()
)
```

### Envoyer un Message de Test
```
URL: http://127.0.0.1:8000/admin/messages/
1. Sélectionner un driver spécifique
2. Écrire un message
3. Optionnel: Associer un trajet
4. Cliquer "Envoyer"
5. Vérifier apparition dans /driver/messages/
```

---

## 🐛 Dépannage

### Erreur: "TemplateDoesNotExist"
✅ Résolu! Les templates sont maintenant créés.

### Messages ne s'affichent pas
- Vérifier que `driver/messages/` contient des messages en DB
- Vérifier que `recipient=request.user` dans la requête
- Activer les logs Django pour debugging

### Carte Leaflet ne charge pas
- Vérifier la connexion Internet (besoin pour OSM)
- Vérifier console navigateur pour erreurs JS
- Vérifier que `leaflet.js` et CSS sont chargés

---

## ✨ Prochaines Améliorations Possibles

- [ ] Upload photo profile pour les drivers
- [ ] Notifications en temps réel (WebSockets)
- [ ] Historique de trajets exportable (PDF)
- [ ] Statistiques drivers (trajets/jour, temps moyen)
- [ ] Tracking GPS en direct des buses
- [ ] Chat/réponse aux messages pour drivers

