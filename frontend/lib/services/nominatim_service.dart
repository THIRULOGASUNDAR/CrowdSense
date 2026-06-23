/// CrowdSense — Nominatim Service
/// All geocoding and place search goes through this service.
/// Uses https://nominatim.openstreetmap.org (configurable via AppConfig).
///
/// IMPORTANT: Nominatim usage policy requires:
///  1. Max 1 request/second.
///  2. A descriptive User-Agent header with your app name and contact email.
///  3. Do NOT cache-bust or scrape in bulk.

import 'dart:convert';
import 'dart:math' as math;
import 'package:http/http.dart' as http;
import '../core/constants/app_config.dart';
import '../models/place_model.dart';

class NominatimService {
  static const String _userAgent =
      'CrowdSense/1.0 (${AppConfig.supportEmail})';

  final http.Client _client;
  NominatimService({http.Client? client}) : _client = client ?? http.Client();

  /// Search places by query string.
  Future<List<PlaceModel>> searchPlaces(String query,
      {int limit = 20}) async {
    if (query.trim().isEmpty) return [];

    final uri = Uri.parse(AppConfig.nominatimBaseUrl).replace(
      path: '/search',
      queryParameters: {
        'q':              query,
        'format':         'jsonv2',
        'addressdetails': '1',
        'namedetails':    '1',
        'limit':          limit.toString(),
        'dedupe':         '1',
        'countrycodes':   'in',
      },
    );

    try {
      final response = await _client.get(uri, headers: {
        'User-Agent': _userAgent,
        'Accept-Language': 'en',
      });

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) =>
            PlaceModel.fromNominatim(json as Map<String, dynamic>)).toList();
      }
      throw Exception('Nominatim error ${response.statusCode}');
    } catch (e) {
      throw Exception('Place search failed: $e');
    }
  }

  /// Reverse geocode a lat/lng to an address string.
  Future<String?> reverseGeocode(double lat, double lng) async {
    final uri = Uri.parse(AppConfig.nominatimBaseUrl).replace(
      path: '/reverse',
      queryParameters: {
        'lat':    lat.toString(),
        'lon':    lng.toString(),
        'format': 'jsonv2',
      },
    );

    try {
      final response = await _client.get(uri, headers: {
        'User-Agent': _userAgent,
      });
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        return data['display_name'] as String?;
      }
    } catch (_) {}
    return null;
  }

  /// Calculate straight-line distance between two points (Haversine formula).
  static double haversineDistanceKm(
      double lat1, double lng1, double lat2, double lng2) {
    const double R = 6371;
    final double dLat = _toRad(lat2 - lat1);
    final double dLng = _toRad(lng2 - lng1);
    final double a = math.sin(dLat / 2) * math.sin(dLat / 2) +
        math.sin(dLng / 2) * math.sin(dLng / 2) * math.cos(_toRad(lat1)) * math.cos(_toRad(lat2));
    final double c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    return R * c;
  }

  static double _toRad(double deg) => deg * math.pi / 180;
}
