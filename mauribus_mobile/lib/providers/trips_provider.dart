import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class TripsProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Trip> _trips = [];
  List<Trip> _filteredTrips = [];
  Trip? _selectedTrip;
  bool _isLoading = false;
  String? _error;
  int? _selectedLineId;

  List<Trip> get trips => _filteredTrips.isEmpty ? _trips : _filteredTrips;
  Trip? get selectedTrip => _selectedTrip;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchTrips({int? lineId}) async {
    _isLoading = true;
    _error = null;
    _selectedLineId = lineId;
    notifyListeners();

    try {
      _trips = await _apiService.getTrips(lineId: lineId);
      _filteredTrips = [];
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  void selectTrip(Trip trip) {
    _selectedTrip = trip;
    notifyListeners();
  }

  void filterByStatus(String status) {
    if (status == 'all') {
      _filteredTrips = [];
    } else {
      _filteredTrips = _trips.where((trip) => trip.status == status).toList();
    }
    notifyListeners();
  }

  void filterByAvailability(bool availableOnly) {
    if (availableOnly) {
      _filteredTrips = _trips.where((trip) => trip.availableSeats > 0).toList();
    } else {
      _filteredTrips = [];
    }
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
