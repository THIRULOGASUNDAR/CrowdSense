import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/place_model.dart';
import '../models/travel_plan_model.dart';
import '../services/nominatim_service.dart';
import '../core/utils/crowd_predictor.dart';
import '../core/constants/app_config.dart';

class TravelPlannerProvider extends ChangeNotifier {
  PlaceModel? _source;
  PlaceModel? _destination;
  TravelPlanModel? _plan;
  bool _isCalculating = false;

  PlaceModel? get source => _source;
  PlaceModel? get destination => _destination;
  TravelPlanModel? get plan => _plan;
  bool get isCalculating => _isCalculating;

  void setSource(PlaceModel place) {
    _source = place;
    notifyListeners();
  }

  void setDestination(PlaceModel place) {
    _destination = place;
    notifyListeners();
  }

  Future<void> calculatePlan() async {
    if (_source == null || _destination == null) return;

    _isCalculating = true;
    notifyListeners();

    try {
      final distance = NominatimService.haversineDistanceKm(
        _source!.latitude, _source!.longitude,
        _destination!.latitude, _destination!.longitude,
      );

      // Estimate 50 km/h avg speed
      final estimatedMinutes = ((distance / 50) * 60).round();

      // Use CrowdPredictor for recommended visit time
      final prediction = CrowdPredictor.predict(
        dateTime: DateTime.now(),
        recentReports: [], // Simplified for now
      );

      final user = FirebaseAuth.instance.currentUser;
      
      _plan = TravelPlanModel(
        id: '',
        userId: user?.uid ?? 'guest',
        sourceName: _source!.name,
        sourceLat: _source!.latitude,
        sourceLng: _source!.longitude,
        destinationName: _destination!.name,
        destinationLat: _destination!.latitude,
        destinationLng: _destination!.longitude,
        distanceKm: distance,
        estimatedMinutes: estimatedMinutes,
        recommendedVisitTime: prediction.bestTimeToVisit,
        createdAt: DateTime.now(),
      );

      if (user != null) {
        await FirebaseFirestore.instance
            .collection(AppConfig.travelPlansCollection)
            .add(_plan!.toMap());
      }

    } catch (e) {
      debugPrint('Error calculating plan: $e');
    } finally {
      _isCalculating = false;
      notifyListeners();
    }
  }

  void clear() {
    _source = null;
    _destination = null;
    _plan = null;
    notifyListeners();
  }
}
