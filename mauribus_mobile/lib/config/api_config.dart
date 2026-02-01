import 'package:flutter/foundation.dart';

// Configuration API
class ApiConfig {
  // IMPORTANT :
  // - Web (Chrome) => localhost
  // - Mobile (Android/iOS) => IP locale du PC (LAN)
  static String get baseUrl {
    if (kIsWeb) {
      return 'http://127.0.0.1:8000';
    }
    return 'http://192.168.1.100:8000'; // ← Remplacez par votre IP locale
  }
  // static const String baseUrl = 'https://api.mauribus.com'; // Production
  
  // Endpoints
  static String get loginEndpoint => '$baseUrl/api/auth/login/';
  static String get registerEndpoint => '$baseUrl/api/auth/register/';
  static String get linesEndpoint => '$baseUrl/api/lines/';
  static String get tripsEndpoint => '$baseUrl/api/trips/';
  static String get bookingsEndpoint => '$baseUrl/api/bookings/';
  static String get userProfileEndpoint => '$baseUrl/api/user/profile/';
  
  // Timeouts
  static const int connectionTimeout = 30; // secondes
  static const int receiveTimeout = 30;
  
  // API Version
  static const String apiVersion = 'v1';
}

// Erreurs API
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final dynamic originalException;

  ApiException({
    required this.message,
    this.statusCode,
    this.originalException,
  });

  @override
  String toString() => 'ApiException: $message (status: $statusCode)';
}

// Réponse générécale API
class ApiResponse<T> {
  final bool success;
  final T? data;
  final String? message;
  final int? statusCode;

  ApiResponse({
    required this.success,
    this.data,
    this.message,
    this.statusCode,
  });

  factory ApiResponse.fromJson(Map<String, dynamic> json, T Function(dynamic) fromJsonT) {
    return ApiResponse(
      success: json['success'] ?? false,
      data: json['data'] != null ? fromJsonT(json['data']) : null,
      message: json['message'],
      statusCode: json['status_code'],
    );
  }
}
