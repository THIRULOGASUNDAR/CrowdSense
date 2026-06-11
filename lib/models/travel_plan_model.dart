import 'package:cloud_firestore/cloud_firestore.dart';

class TravelPlanModel {
  final String id;
  final String userId;
  final String sourceName;
  final double sourceLat;
  final double sourceLng;
  final String destinationName;
  final double destinationLat;
  final double destinationLng;
  final double distanceKm;
  final int estimatedMinutes;
  final String recommendedVisitTime;
  final DateTime createdAt;

  const TravelPlanModel({
    required this.id,
    required this.userId,
    required this.sourceName,
    required this.sourceLat,
    required this.sourceLng,
    required this.destinationName,
    required this.destinationLat,
    required this.destinationLng,
    required this.distanceKm,
    required this.estimatedMinutes,
    required this.recommendedVisitTime,
    required this.createdAt,
  });

  factory TravelPlanModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return TravelPlanModel(
      id: doc.id,
      userId: data['userId'] ?? '',
      sourceName: data['sourceName'] ?? '',
      sourceLat: (data['sourceLat'] as num?)?.toDouble() ?? 0.0,
      sourceLng: (data['sourceLng'] as num?)?.toDouble() ?? 0.0,
      destinationName: data['destinationName'] ?? '',
      destinationLat: (data['destinationLat'] as num?)?.toDouble() ?? 0.0,
      destinationLng: (data['destinationLng'] as num?)?.toDouble() ?? 0.0,
      distanceKm: (data['distanceKm'] as num?)?.toDouble() ?? 0.0,
      estimatedMinutes: data['estimatedMinutes'] ?? 0,
      recommendedVisitTime: data['recommendedVisitTime'] ?? '',
      createdAt: (data['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toMap() => {
    'userId': userId,
    'sourceName': sourceName,
    'sourceLat': sourceLat,
    'sourceLng': sourceLng,
    'destinationName': destinationName,
    'destinationLat': destinationLat,
    'destinationLng': destinationLng,
    'distanceKm': distanceKm,
    'estimatedMinutes': estimatedMinutes,
    'recommendedVisitTime': recommendedVisitTime,
    'createdAt': FieldValue.serverTimestamp(),
  };
}
