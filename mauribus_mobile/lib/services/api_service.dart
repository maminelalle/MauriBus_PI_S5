import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/api_config.dart';
import '../models/models.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  
  factory ApiService() {
    return _instance;
  }
  
  ApiService._internal();

  String? _token;
  late SharedPreferences _prefs;

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
    _token = _prefs.getString('auth_token');
  }

  // ===== AUTHENTIFICATION =====

  Future<String> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.loginEndpoint),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
        }),
      ).timeout(const Duration(seconds: ApiConfig.connectionTimeout));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _token = data['token'];
        await _prefs.setString('auth_token', _token!);
        return _token!;
      } else {
        try {
          final data = jsonDecode(response.body);
          throw ApiException(
            message: data['error'] ?? 'Erreur de connexion (${response.statusCode})',
            statusCode: response.statusCode,
          );
        } catch (e) {
          if (e is ApiException) rethrow;
          throw ApiException(
            message: 'Erreur de connexion: ${response.body}',
            statusCode: response.statusCode,
          );
        }
      }
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau: ${e.toString()}',
        originalException: e,
      );
    }
  }

  Future<String> register(String email, String password, String firstName, String lastName) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.registerEndpoint),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
          'first_name': firstName,
          'last_name': lastName,
        }),
      ).timeout(const Duration(seconds: ApiConfig.connectionTimeout));

      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        _token = data['token'];
        await _prefs.setString('auth_token', _token!);
        return _token!;
      } else {
        try {
          final data = jsonDecode(response.body);
          throw ApiException(
            message: data['error'] ?? 'Erreur lors de l\'inscription (${response.statusCode})',
            statusCode: response.statusCode,
          );
        } catch (e) {
          if (e is ApiException) rethrow;
          throw ApiException(
            message: 'Erreur lors de l\'inscription: ${response.body}',
            statusCode: response.statusCode,
          );
        }
      }
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau: ${e.toString()}',
        originalException: e,
      );
    }
  }

  Future<void> logout() async {
    _token = null;
    await _prefs.remove('auth_token');
  }

  bool get isAuthenticated => _token != null;
  String? get token => _token;

  // ===== LIGNES =====

  Future<List<Line>> getLines() async {
    try {
      final response = await http.get(
        Uri.parse(ApiConfig.linesEndpoint),
        headers: _headers(),
      ).timeout(const Duration(seconds: ApiConfig.receiveTimeout));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((line) => Line.fromJson(line)).toList();
      } else {
        throw ApiException(
          message: 'Impossible de charger les lignes',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  Future<Line> getLine(int id) async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.linesEndpoint}$id/'),
        headers: _headers(),
      ).timeout(const Duration(seconds: ApiConfig.receiveTimeout));

      if (response.statusCode == 200) {
        return Line.fromJson(jsonDecode(response.body));
      } else {
        throw ApiException(
          message: 'Ligne non trouvée',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  // ===== TRAJETS =====

  Future<List<Trip>> getTrips({int? lineId}) async {
    try {
      String url = ApiConfig.tripsEndpoint;
      if (lineId != null) {
        url += '?line_id=$lineId';
      }
      
      final response = await http.get(
        Uri.parse(url),
        headers: _headers(),
      ).timeout(const Duration(seconds: ApiConfig.receiveTimeout));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((trip) => Trip.fromJson(trip)).toList();
      } else {
        throw ApiException(
          message: 'Impossible de charger les trajets',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  // ===== RÉSERVATIONS =====

  Future<Booking> createBooking(int tripId, int numberOfSeats) async {
    try {
      final response = await http.post(
        Uri.parse(ApiConfig.bookingsEndpoint),
        headers: _headers(),
        body: jsonEncode({
          'trip_id': tripId,
          'number_of_seats': numberOfSeats,
        }),
      ).timeout(const Duration(seconds: ApiConfig.connectionTimeout));

      if (response.statusCode == 201) {
        return Booking.fromJson(jsonDecode(response.body));
      } else {
        throw ApiException(
          message: 'Erreur lors de la réservation',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  Future<List<Booking>> getUserBookings() async {
    try {
      final response = await http.get(
        Uri.parse(ApiConfig.bookingsEndpoint),
        headers: _headers(),
      ).timeout(const Duration(seconds: ApiConfig.receiveTimeout));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List;
        return data.map((booking) => Booking.fromJson(booking)).toList();
      } else {
        throw ApiException(
          message: 'Impossible de charger les réservations',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  // ===== PROFIL =====

  Future<User> getUserProfile() async {
    try {
      final response = await http.get(
        Uri.parse(ApiConfig.userProfileEndpoint),
        headers: _headers(),
      ).timeout(const Duration(seconds: ApiConfig.receiveTimeout));

      if (response.statusCode == 200) {
        return User.fromJson(jsonDecode(response.body));
      } else {
        throw ApiException(
          message: 'Impossible de charger le profil',
          statusCode: response.statusCode,
        );
      }
    } catch (e) {
      throw ApiException(
        message: 'Erreur réseau',
        originalException: e,
      );
    }
  }

  // ===== HELPER =====

  Map<String, String> _headers() {
    return {
      'Content-Type': 'application/json',
      if (_token != null) 'Authorization': 'Bearer $_token',
    };
  }
}
