import 'package:flutter/material.dart';
import '../models/models.dart';
import '../services/api_service.dart';

class LinesProvider extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  
  List<Line> _lines = [];
  bool _isLoading = false;
  String? _error;

  List<Line> get lines => _lines;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> fetchLines() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lines = await _apiService.getLines();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<Line?> getLineDetails(int id) async {
    try {
      return await _apiService.getLine(id);
    } catch (e) {
      _error = e.toString();
      notifyListeners();
      return null;
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
