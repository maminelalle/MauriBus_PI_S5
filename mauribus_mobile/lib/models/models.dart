// Models pour les données

// Ligne de transport
class Line {
  final int id;
  final String name;
  final String description;
  final String startLocation;
  final String endLocation;
  final double startLat;
  final double startLng;
  final double endLat;
  final double endLng;
  final double price;
  final int estimatedDuration; // en minutes

  Line({
    required this.id,
    required this.name,
    required this.description,
    required this.startLocation,
    required this.endLocation,
    required this.startLat,
    required this.startLng,
    required this.endLat,
    required this.endLng,
    required this.price,
    required this.estimatedDuration,
  });

  factory Line.fromJson(Map<String, dynamic> json) {
    return Line(
      id: json['id'],
      name: json['name'],
      description: json['description'] ?? '',
      startLocation: json['start_location'] ?? '',
      endLocation: json['end_location'] ?? '',
      startLat: (json['start_lat'] as num?)?.toDouble() ?? 0,
      startLng: (json['start_lng'] as num?)?.toDouble() ?? 0,
      endLat: (json['end_lat'] as num?)?.toDouble() ?? 0,
      endLng: (json['end_lng'] as num?)?.toDouble() ?? 0,
      price: (json['price'] as num?)?.toDouble() ?? 0,
      estimatedDuration: json['estimated_duration'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'description': description,
    'start_location': startLocation,
    'end_location': endLocation,
    'start_lat': startLat,
    'start_lng': startLng,
    'end_lat': endLat,
    'end_lng': endLng,
    'price': price,
    'estimated_duration': estimatedDuration,
  };
}

// Trajet/Voyage
class Trip {
  final int id;
  final int lineId;
  final int busId;
  final String busName;
  final String driverName;
  final DateTime departureTime;
  final DateTime? arrivalTime;
  final String status; // 'pending', 'ongoing', 'completed', 'cancelled'
  final int availableSeats;
  final int totalSeats;

  Trip({
    required this.id,
    required this.lineId,
    required this.busId,
    required this.busName,
    required this.driverName,
    required this.departureTime,
    this.arrivalTime,
    required this.status,
    required this.availableSeats,
    required this.totalSeats,
  });

  factory Trip.fromJson(Map<String, dynamic> json) {
    return Trip(
      id: json['id'],
      lineId: json['line_id'],
      busId: json['bus_id'],
      busName: json['bus_name'] ?? '',
      driverName: json['driver_name'] ?? '',
      departureTime: DateTime.parse(json['departure_time']),
      arrivalTime: json['arrival_time'] != null ? DateTime.parse(json['arrival_time']) : null,
      status: json['status'] ?? 'pending',
      availableSeats: json['available_seats'] ?? 0,
      totalSeats: json['total_seats'] ?? 50,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'line_id': lineId,
    'bus_id': busId,
    'bus_name': busName,
    'driver_name': driverName,
    'departure_time': departureTime.toIso8601String(),
    'arrival_time': arrivalTime?.toIso8601String(),
    'status': status,
    'available_seats': availableSeats,
    'total_seats': totalSeats,
  };

  bool get isFull => availableSeats <= 0;
  int get occupiedSeats => totalSeats - availableSeats;
  double get occupancyPercentage => (occupiedSeats / totalSeats) * 100;
}

// Réservation
class Booking {
  final int id;
  final int tripId;
  final int userId;
  final int numberOfSeats;
  final double totalPrice;
  final String status; // 'pending', 'confirmed', 'cancelled'
  final DateTime bookingDate;
  final String? ticketCode;

  Booking({
    required this.id,
    required this.tripId,
    required this.userId,
    required this.numberOfSeats,
    required this.totalPrice,
    required this.status,
    required this.bookingDate,
    this.ticketCode,
  });

  factory Booking.fromJson(Map<String, dynamic> json) {
    return Booking(
      id: json['id'],
      tripId: json['trip_id'],
      userId: json['user_id'],
      numberOfSeats: json['number_of_seats'],
      totalPrice: (json['total_price'] as num?)?.toDouble() ?? 0,
      status: json['status'] ?? 'pending',
      bookingDate: DateTime.parse(json['booking_date']),
      ticketCode: json['ticket_code'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'trip_id': tripId,
    'user_id': userId,
    'number_of_seats': numberOfSeats,
    'total_price': totalPrice,
    'status': status,
    'booking_date': bookingDate.toIso8601String(),
    'ticket_code': ticketCode,
  };
}

// Utilisateur
class User {
  final int id;
  final String email;
  final String firstName;
  final String lastName;
  final String? phone;
  final String? photoUrl;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.firstName,
    required this.lastName,
    this.phone,
    this.photoUrl,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      phone: json['phone'],
      photoUrl: json['photo_url'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'first_name': firstName,
    'last_name': lastName,
    'phone': phone,
    'photo_url': photoUrl,
    'created_at': createdAt.toIso8601String(),
  };

  String get fullName => '$firstName $lastName';
}
