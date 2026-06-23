import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:latlong2/latlong.dart';
import '../models/place_model.dart';
import '../models/travel_plan_model.dart';
import '../services/nominatim_service.dart';
import '../services/osrm_service.dart';
import '../core/utils/crowd_predictor.dart';
import '../core/constants/app_config.dart';

class TravelPlannerProvider extends ChangeNotifier {
  PlaceModel? _source;
  PlaceModel? _destination;
  TravelPlanModel? _plan;
  bool _isCalculating = false;
  List<LatLng> _routeCoordinates = [];

  PlaceModel? get source => _source;
  PlaceModel? get destination => _destination;
  TravelPlanModel? get plan => _plan;
  bool get isCalculating => _isCalculating;
  List<LatLng> get routeCoordinates => _routeCoordinates;

  final OsrmService _osrmService = OsrmService();

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
      final sourceLatLng = LatLng(_source!.latitude, _source!.longitude);
      final destLatLng = LatLng(_destination!.latitude, _destination!.longitude);
      
      final osrmRoute = await _osrmService.getRoute(sourceLatLng, destLatLng);
      
      // Use CrowdPredictor for recommended visit time
      final prediction = CrowdPredictor.predict(
        dateTime: DateTime.now(),
        recentReports: [], // Simplified for now
      );

      double distance = 0.0;
      int estimatedMinutes = 0;
      
      if (osrmRoute != null) {
        // OSRM uses shortest-path and free-flow speeds, which differs significantly from Google Maps in cities.
        // Apply city-traffic correction heuristics to match realistic arterial routing (e.g., Google Maps).
        distance = osrmRoute.distanceKm * 1.163; // Scaling factor to match arterial roads
        
        // Base city traffic is typically 2.5x slower than free-flow. Adjust slightly based on crowd score.
        double crowdMultiplier = 2.0 + (prediction.score / 100.0); // Ranges from 2.0x to 3.0x
        estimatedMinutes = (osrmRoute.estimatedMinutes * crowdMultiplier).round();
        
        _routeCoordinates = osrmRoute.coordinates;
      } else {
        // Fallback to Haversine speed estimate
        distance = NominatimService.haversineDistanceKm(
          _source!.latitude, _source!.longitude,
          _destination!.latitude, _destination!.longitude,
        );
        estimatedMinutes = ((distance / 50) * 60).round();
        _routeCoordinates = [sourceLatLng, destLatLng];
      }

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
    _routeCoordinates = [];
    notifyListeners();
  }
}
