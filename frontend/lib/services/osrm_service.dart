import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:latlong2/latlong.dart';

class OsrmRoute {
  final double distanceKm;
  final int estimatedMinutes;
  final List<LatLng> coordinates;

  OsrmRoute({
    required this.distanceKm,
    required this.estimatedMinutes,
    required this.coordinates,
  });
}

class OsrmService {
  static const String _baseUrl = 'http://router.project-osrm.org/route/v1/driving';

  Future<OsrmRoute?> getRoute(LatLng source, LatLng destination) async {
    final url = '$_baseUrl/${source.longitude},${source.latitude};${destination.longitude},${destination.latitude}?overview=full&geometries=geojson';
    
    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['routes'] != null && data['routes'].isNotEmpty) {
          final route = data['routes'][0];
          
          // Distance is in meters
          final distanceKm = (route['distance'] as num).toDouble() / 1000.0;
          
          // Duration is in seconds
          final durationSec = (route['duration'] as num).toDouble();
          final estimatedMinutes = (durationSec / 60).round();
          
          final coordinates = <LatLng>[];
          final geometry = route['geometry'];
          if (geometry != null && geometry['type'] == 'LineString') {
            final coords = geometry['coordinates'] as List;
            for (var coord in coords) {
              coordinates.add(LatLng((coord[1] as num).toDouble(), (coord[0] as num).toDouble()));
            }
          }
          
          return OsrmRoute(
            distanceKm: distanceKm,
            estimatedMinutes: estimatedMinutes,
            coordinates: coordinates,
          );
        }
      }
    } catch (e) {
      print('Error fetching OSRM route: $e');
    }
    return null;
  }
}
