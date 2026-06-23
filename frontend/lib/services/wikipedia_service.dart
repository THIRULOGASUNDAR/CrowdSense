import 'dart:convert';
import 'package:http/http.dart' as http;

class WikipediaService {
  static const String _userAgent = 'CrowdSense/1.0';

  /// Fetches a real image from Wikipedia for a given place name.
  /// Returns the image URL if found, otherwise returns null.
  static Future<String?> fetchPlaceImageUrl(String query) async {
    if (query.trim().isEmpty) return null;
    try {
      final encodedQuery = Uri.encodeComponent(query);
      final url = Uri.parse('https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch=$encodedQuery&gsrlimit=1&prop=pageimages&format=json&pithumbsize=600&origin=*');
      
      final response = await http.get(url, headers: {'User-Agent': _userAgent});
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final pages = data['query']?['pages'] as Map<String, dynamic>?;
        if (pages != null && pages.isNotEmpty) {
          final page = pages.values.first;
          final thumbnail = page['thumbnail'];
          if (thumbnail != null && thumbnail['source'] != null) {
            return thumbnail['source'] as String;
          }
        }
      }
    } catch (e) {
      // Ignore errors, return null to fallback smoothly
    }
    return null;
  }
}
