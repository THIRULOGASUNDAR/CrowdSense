import 'package:cloud_firestore/cloud_firestore.dart';

/// Represents a place returned from Nominatim or stored in Firestore.
class PlaceModel {
  final String id;
  final String name;
  final String displayName;
  final String? description;
  final double latitude;
  final double longitude;
  final String? category;       // e.g. 'tourism', 'restaurant', 'park'
  final String? thumbnailUrl;
  final List<String> photoUrls;
  final double rating;
  final int totalReviews;
  final int crowdScore;          // 0–100, updated by Firestore trigger
  final DateTime? updatedAt;

  const PlaceModel({
    required this.id,
    required this.name,
    required this.displayName,
    this.description,
    required this.latitude,
    required this.longitude,
    this.category,
    this.thumbnailUrl,
    this.photoUrls = const [],
    this.rating = 0.0,
    this.totalReviews = 0,
    this.crowdScore = 0,
    this.updatedAt,
  });

  /// Build from a Nominatim JSON result.
  factory PlaceModel.fromNominatim(Map<String, dynamic> json) {
    return PlaceModel(
      id:           json['place_id'].toString(),
      name:         _extractName(json),
      displayName:  json['display_name'] ?? '',
      latitude:     double.tryParse(json['lat'] ?? '0') ?? 0,
      longitude:    double.tryParse(json['lon'] ?? '0') ?? 0,
      category:     json['category'] ?? json['type'],
    );
  }

  /// Build from a Firestore document.
  factory PlaceModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return PlaceModel(
      id:           doc.id,
      name:         data['name'] ?? '',
      displayName:  data['displayName'] ?? '',
      description:  data['description'],
      latitude:     (data['latitude'] as num?)?.toDouble() ?? 0,
      longitude:    (data['longitude'] as num?)?.toDouble() ?? 0,
      category:     data['category'],
      thumbnailUrl: data['thumbnailUrl'],
      photoUrls:    List<String>.from(data['photoUrls'] ?? []),
      rating:       (data['rating'] as num?)?.toDouble() ?? 0,
      totalReviews: data['totalReviews'] ?? 0,
      crowdScore:   data['crowdScore'] ?? 0,
      updatedAt:    (data['updatedAt'] as Timestamp?)?.toDate(),
    );
  }

  Map<String, dynamic> toMap() => {
    'name':         name,
    'displayName':  displayName,
    'description':  description,
    'latitude':     latitude,
    'longitude':    longitude,
    'category':     category,
    'thumbnailUrl': thumbnailUrl,
    'photoUrls':    photoUrls,
    'rating':       rating,
    'totalReviews': totalReviews,
    'crowdScore':   crowdScore,
    'updatedAt':    FieldValue.serverTimestamp(),
  };

  /// Returns a related description if the actual description is empty.
  String get relatedDescription {
    if (description != null && description!.isNotEmpty) return description!;
    
    final cat = category?.toLowerCase() ?? '';
    if (cat.contains('park')) {
      return '$name is a beautiful green space perfect for relaxation, morning walks, and enjoying nature away from the city noise.';
    } else if (cat.contains('restaurant') || cat.contains('cafe')) {
      return '$name is a popular local spot offering a great atmosphere and delicious food. Check our crowd predictions to find the quietest time to dine.';
    } else if (cat.contains('tourism') || cat.contains('monument') || cat.contains('landmark')) {
      return '$name is a significant landmark and a must-visit attraction. Use CrowdSense to avoid the peak tourist hours and enjoy a peaceful experience.';
    } else if (cat.contains('museum') || cat.contains('art')) {
      return 'Explore the rich culture and history at $name. Our real-time crowd data helps you enjoy the exhibits without the heavy crowds.';
    } else if (cat.contains('shop') || cat.contains('mall')) {
      return '$name offers a variety of shopping and retail experiences. Plan your visit during off-peak hours for a more comfortable shopping trip.';
    } else {
      return '$name is a notable location in this area. CrowdSense provides AI-powered crowd predictions to help you plan your visit and avoid crowded times.';
    }
  }

  static String _extractName(Map<String, dynamic> json) {
    final tags = json['namedetails'] as Map<String, dynamic>?;
    if (tags != null && tags['name'] != null) return tags['name'];
    final display = json['display_name'] as String? ?? '';
    return display.split(',').first.trim();
  }

  PlaceModel copyWith({int? crowdScore, double? rating, int? totalReviews}) {
    return PlaceModel(
      id: id, name: name, displayName: displayName,
      description: description, latitude: latitude, longitude: longitude,
      category: category, thumbnailUrl: thumbnailUrl, photoUrls: photoUrls,
      rating: rating ?? this.rating,
      totalReviews: totalReviews ?? this.totalReviews,
      crowdScore: crowdScore ?? this.crowdScore,
      updatedAt: updatedAt,
    );
  }
}
