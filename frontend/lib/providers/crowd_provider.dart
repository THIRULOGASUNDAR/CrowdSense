import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/crowd_report_model.dart';
import '../services/firestore_service.dart';
import '../services/crowd_prediction_service.dart';
import '../core/utils/crowd_predictor.dart';

class CrowdProvider extends ChangeNotifier {
  final FirestoreService _firestoreService = FirestoreService();
  final CrowdPredictionService _predictionService = CrowdPredictionService();

  CrowdPrediction? _currentPrediction;
  List<int> _hourlyForecast = [];
  List<CrowdReportModel> _recentReports = [];
  bool _isLoading = false;
  StreamSubscription<List<CrowdReportModel>>? _reportsSubscription;

  CrowdPrediction? get currentPrediction => _currentPrediction;
  List<int> get hourlyForecast => _hourlyForecast;
  List<CrowdReportModel> get recentReports => _recentReports;
  bool get isLoading => _isLoading;

  Future<void> loadPrediction(String placeId) async {
    _isLoading = true;
    notifyListeners();

    try {
      _currentPrediction = await _predictionService.getPrediction(placeId);
      
      // Cancel previous subscription to avoid memory leaks and multiple listeners
      await _reportsSubscription?.cancel();

      // Load recent reports stream
      _reportsSubscription = _firestoreService.getRecentReports(placeId).listen((reports) {
        _recentReports = reports;
        final scores = reports.map((r) => r.level.score).toList();

        // Update the current prediction locally when new reports arrive
        if (_currentPrediction != null) {
          _currentPrediction = CrowdPredictor.predict(
            dateTime: DateTime.now(),
            recentReports: scores,
            historicalBaseline: _currentPrediction!.baseline,
            bestTimeToVisit: _currentPrediction!.bestTimeToVisit,
          );
        }
        
        // Generate hourly forecast based on reports using the same dynamic baseline
        _hourlyForecast = CrowdPredictor.predictDayForecast(
          weekday: DateTime.now().weekday,
          recentReports: scores,
          historicalBaseline: _currentPrediction?.baseline ?? 50,
        );

        notifyListeners();
      });
    } catch (e) {
      debugPrint('Error loading prediction: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> submitReport(String placeId, CrowdReportLevel level, {String? note}) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    final report = CrowdReportModel(
      id: '',
      placeId: placeId,
      userId: user.uid,
      userName: user.displayName ?? 'Anonymous',
      level: level,
      note: note,
      reportedAt: DateTime.now(),
    );

    try {
      await _firestoreService.submitCrowdReport(report);
      // Removed await loadPrediction(placeId); here since the stream listener will automatically
      // receive the new report and update the UI accordingly.
    } catch (e) {
      debugPrint('Error submitting report: $e');
    }
  }

  @override
  void dispose() {
    _reportsSubscription?.cancel();
    super.dispose();
  }
}
