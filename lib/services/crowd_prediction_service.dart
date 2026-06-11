import 'firestore_service.dart';
import '../core/utils/crowd_predictor.dart';
import '../models/crowd_report_model.dart';

class CrowdPredictionService {
  final FirestoreService _firestoreService = FirestoreService();

  Future<CrowdPrediction> getPrediction(String placeId) async {
    // 1. Get recent reports from last 24 hours
    final reports = await _firestoreService.getRecentReports(placeId).first;
    final scores = reports.map((r) => r.level.score).toList();

    // 2. Predict using local engine
    return CrowdPredictor.predict(
      dateTime: DateTime.now(),
      recentReports: scores,
      historicalBaseline: 50, // This could be fetched from place model
    );
  }
}
