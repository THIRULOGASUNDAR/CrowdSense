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
  final String? _thumbnailUrl;
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
    String? thumbnailUrl,
    this.photoUrls = const [],
    this.rating = 0.0,
    this.totalReviews = 0,
    this.crowdScore = 0,
    this.updatedAt,
  }) : _thumbnailUrl = thumbnailUrl;

  String? get thumbnailUrl {
    if (_thumbnailUrl != null && !_thumbnailUrl!.contains('picsum.photos') && !_thumbnailUrl!.contains('photo-1524008279394') && !_thumbnailUrl!.contains('photo-1472214222555')) {
      return _thumbnailUrl;
    }
    return _generatePlaceImageUrl(name, displayName, category);
  }

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

  static String _generatePlaceImageUrl(String name, String displayName, String? category) {
    final cleanName = name.toLowerCase();
    final cleanCat = (category ?? '').toLowerCase();
    final hash = (name + displayName).hashCode.abs();
    
    String pick(List<String> urls) => urls[hash % urls.length];

    // Keyword check for specific famous landmarks
    if (cleanName.contains('eiffel') || cleanName.contains('paris')) {
      return 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('central park')) {
      return 'https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('london eye') || (cleanName.contains('london') && cleanCat.contains('tourism'))) {
      return 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('taj mahal') || cleanName.contains('agra')) {
      return 'https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('colosseum') || cleanName.contains('rome')) {
      return 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('statue of liberty') || cleanName.contains('liberty island')) {
      return 'https://images.unsplash.com/photo-1605130284535-11dd9eedc58a?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('opera house') || cleanName.contains('sydney')) {
      return 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('fuji') || cleanName.contains('tokyo')) {
      return 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('beach') || cleanName.contains('marina') || cleanName.contains('coast') || cleanName.contains('island')) {
      return 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&auto=format&fit=crop&q=80';
    } else if (cleanName.contains('waterfall') || cleanName.contains('falls') || cleanName.contains('niagara')) {
      return 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=600&auto=format&fit=crop&q=80';
    }

    // Category fallback check with lists for uniqueness
    if (cleanCat.contains('park') || cleanName.contains('park') || cleanCat.contains('garden') || cleanCat.contains('nature') || cleanCat.contains('forest')) {
      return pick([
        'https://images.unsplash.com/photo-1448375240586-882707db888b?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1519331379826-f10be5486c6f?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1473448912268-2022ce9509d8?w=600&auto=format&fit=crop&q=80'
      ]);
    } else if (cleanCat.contains('restaurant') || cleanName.contains('restaurant') || cleanCat.contains('cafe') || cleanName.contains('cafe') || cleanName.contains('coffee') || cleanCat.contains('food') || cleanCat.contains('bakery') || cleanCat.contains('bar') || cleanCat.contains('pub')) {
      return pick([
        'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1559925393-8be0ec4767c8?w=600&auto=format&fit=crop&q=80'
      ]);
    } else if (cleanCat.contains('tourism') || cleanCat.contains('attraction') || cleanCat.contains('monument') || cleanCat.contains('landmark') || cleanCat.contains('historic')) {
      return pick([
        'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=600&auto=format&fit=crop&q=80',
        'https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?w=600&auto=format&fit=crop&q=80'
      ]);
    } else if (cleanCat.contains('museum') || cleanCat.contains('art') || cleanCat.contains('gallery') || cleanCat.contains('theatre')) {
      return 'https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=600&auto=format&fit=crop&q=80';
    } else if (cleanCat.contains('shop') || cleanCat.contains('mall') || cleanCat.contains('store') || cleanCat.contains('supermarket')) {
      return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600&auto=format&fit=crop&q=80';
    } else if (cleanCat.contains('hotel') || cleanCat.contains('motel') || cleanCat.contains('resort') || cleanCat.contains('apartment')) {
      return 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80';
    } else if (cleanCat.contains('station') || cleanCat.contains('airport') || cleanCat.contains('railway') || cleanCat.contains('subway') || cleanCat.contains('bus')) {
      return 'https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=600&auto=format&fit=crop&q=80';
    }

    return pick([
      'https://images.unsplash.com/photo-1449844908441-8829872d2607?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1514565131-fce0801e5785?w=600&auto=format&fit=crop&q=80'
    ]);
  }
}
