/// CrowdSense — App Configuration
/// Replace placeholder values with your actual Firebase and API credentials.
class AppConfig {
  AppConfig._();

  // ─── Nominatim (OpenStreetMap geocoding) ──────────────────────────────────
  static const String nominatimBaseUrl = 'https://nominatim.openstreetmap.org';
  // Default public endpoint: 'https://nominatim.openstreetmap.org'
  // Add a custom User-Agent when deploying to production.

  // ─── OpenStreetMap tile template ─────────────────────────────────────────
  static const String osmTileUrl =
      'https://tile.openstreetmap.org/{z}/{x}/{y}.png';

  // ─── Firebase ─────────────────────────────────────────────────────────────
  // Populated automatically by google-services.json / firebase_options.dart.
  // Do NOT hard-code values here. Use FlutterFire CLI:
  //   flutterfire configure
  // which generates lib/firebase_options.dart automatically.

  // ─── App metadata ─────────────────────────────────────────────────────────
  static const String appName       = 'CrowdSense';
  static const String appVersion    = '1.0.0';
  static const String supportEmail  = 'support@crowdsense.app';

  // ─── Firestore collection names ───────────────────────────────────────────
  static const String usersCollection         = 'users';
  static const String placesCollection        = 'places';
  static const String crowdReportsCollection  = 'crowd_reports';
  static const String photosCollection        = 'community_photos';
  static const String reviewsCollection       = 'reviews';
  static const String favoritesCollection     = 'favorites';
  static const String travelPlansCollection   = 'travel_plans';

  // ─── Firebase Storage paths ───────────────────────────────────────────────
  static const String profilePhotosPath   = 'profile_photos';
  static const String communityPhotosPath = 'community_photos';

  // ─── Prediction thresholds ────────────────────────────────────────────────
  static const int lowCrowdThreshold      = 30;   // % score
  static const int moderateCrowdThreshold = 65;
}
