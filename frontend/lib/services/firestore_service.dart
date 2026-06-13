import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/foundation.dart';
import '../models/place_model.dart';
import '../models/crowd_report_model.dart';
import '../models/user_model.dart';
import '../models/review_model.dart';
import '../core/constants/app_config.dart';

class FirestoreService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  // --- Places ---
  Future<PlaceModel?> getPlace(String placeId) async {
    final doc = await _db.collection(AppConfig.placesCollection).doc(placeId).get();
    if (!doc.exists) return null;
    return PlaceModel.fromFirestore(doc);
  }

  Future<void> upsertPlace(PlaceModel place) async {
    await _db.collection(AppConfig.placesCollection).doc(place.id).set(
      place.toMap(),
      SetOptions(merge: true),
    );
  }

  Stream<List<PlaceModel>> getTrendingPlaces({int limit = 10}) {
    return _db
        .collection(AppConfig.placesCollection)
        .orderBy('crowdScore', descending: true)
        .limit(limit)
        .snapshots()
        .map((snapshot) =>
            snapshot.docs.map((doc) => PlaceModel.fromFirestore(doc)).toList());
  }

  // --- Crowd Reports ---
  Future<void> submitCrowdReport(CrowdReportModel report) async {
    await _db.collection(AppConfig.crowdReportsCollection).add(report.toMap());
    
    // Increment total reports for user
    await _db.collection(AppConfig.usersCollection).doc(report.userId).update({
      'totalReports': FieldValue.increment(1),
    });
  }

  Stream<List<CrowdReportModel>> getRecentReports(String placeId, {int hours = 24}) {
    final startTime = DateTime.now().subtract(Duration(hours: hours));
    return _db
        .collection(AppConfig.crowdReportsCollection)
        .where('placeId', isEqualTo: placeId)
        .where('reportedAt', isGreaterThanOrEqualTo: Timestamp.fromDate(startTime))
        .orderBy('reportedAt', descending: true)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => CrowdReportModel.fromFirestore(doc))
            .toList());
  }

  Future<int> getAverageCrowdScore(String placeId) async {
    final startTime = DateTime.now().subtract(const Duration(hours: 24));
    final snapshot = await _db
        .collection(AppConfig.crowdReportsCollection)
        .where('placeId', isEqualTo: placeId)
        .where('reportedAt', isGreaterThanOrEqualTo: Timestamp.fromDate(startTime))
        .get();

    if (snapshot.docs.isEmpty) return 50; // Default baseline

    final totalScore = snapshot.docs.fold<int>(0, (sum, doc) {
      final data = doc.data();
      return sum + (data['score'] as int? ?? 50);
    });

    return (totalScore / snapshot.docs.length).round();
  }

  // --- Favorites ---
  Future<void> addFavorite(String userId, String placeId) async {
    final userDoc = _db.collection(AppConfig.usersCollection).doc(userId);
    final doc = await userDoc.get();
    
    if (!doc.exists) {
      // Create basic user doc if it doesn't exist
      await userDoc.set({
        'savedPlaces': [placeId],
        'totalReports': 0,
        'joinedAt': FieldValue.serverTimestamp(),
      });
    } else {
      await userDoc.update({
        'savedPlaces': FieldValue.arrayUnion([placeId]),
      });
    }
  }

  Future<void> removeFavorite(String userId, String placeId) async {
    await _db.collection(AppConfig.usersCollection).doc(userId).update({
      'savedPlaces': FieldValue.arrayRemove([placeId]),
    });
  }

  Stream<List<String>> getFavoritePlaceIds(String userId) {
    return _db.collection(AppConfig.usersCollection).doc(userId).snapshots().map((doc) {
      if (!doc.exists) return [];
      final data = doc.data() as Map<String, dynamic>;
      return List<String>.from(data['savedPlaces'] ?? []);
    });
  }

  // --- Reviews ---
  Future<void> addReview(ReviewModel review) async {
    await _db.collection(AppConfig.reviewsCollection).add(review.toMap());
    
    // Update place rating (simplified logic)
    final placeDoc = await _db.collection(AppConfig.placesCollection).doc(review.placeId).get();
    if (placeDoc.exists) {
      final place = PlaceModel.fromFirestore(placeDoc);
      final newTotal = place.totalReviews + 1;
      final newRating = ((place.rating * place.totalReviews) + review.rating) / newTotal;
      
      await _db.collection(AppConfig.placesCollection).doc(review.placeId).update({
        'rating': newRating,
        'totalReviews': newTotal,
      });
    }
  }

  Stream<List<ReviewModel>> getReviews(String placeId) {
    return _db
        .collection(AppConfig.reviewsCollection)
        .where('placeId', isEqualTo: placeId)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) =>
            snapshot.docs.map((doc) => ReviewModel.fromFirestore(doc)).toList());
  }

  // --- Profile ---
  Future<UserModel?> getUser(String uid) async {
    final doc = await _db.collection(AppConfig.usersCollection).doc(uid).get();
    if (!doc.exists) return null;
    return UserModel.fromFirestore(doc);
  }

  Future<void> updateUser(UserModel user) async {
    await _db.collection(AppConfig.usersCollection).doc(user.uid).update(user.toMap());
  }
}
