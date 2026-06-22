import 'dart:async';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/place_model.dart';
import '../services/nominatim_service.dart';
import '../services/firestore_service.dart';

class PlaceProvider extends ChangeNotifier {
  final NominatimService _nominatimService = NominatimService();
  final FirestoreService _firestoreService = FirestoreService();

  List<PlaceModel> _searchResults = [];
  List<PlaceModel> _trendingPlaces = [];
  List<String> _recentSearches = [];
  PlaceModel? _selectedPlace;
  bool _isSearching = false;
  bool _isTrendingLoading = false;
  String? _error;
  Timer? _debounce;

  List<PlaceModel> get searchResults => _searchResults;
  List<PlaceModel> get trendingPlaces => _trendingPlaces;
  List<String> get recentSearches => _recentSearches;
  PlaceModel? get selectedPlace => _selectedPlace;
  bool get isSearching => _isSearching;
  bool get isTrendingLoading => _isTrendingLoading;
  String? get error => _error;

  PlaceProvider() {
    _loadRecentSearches();
  }

  Future<void> _loadRecentSearches() async {
    final prefs = await SharedPreferences.getInstance();
    _recentSearches = prefs.getStringList('recent_searches') ?? [];
    notifyListeners();
  }

  Future<void> addRecentSearch(String query) async {
    if (query.trim().isEmpty) return;
    
    _recentSearches.remove(query); // Remove if exists to move to top
    _recentSearches.insert(0, query);
    
    if (_recentSearches.length > 10) {
      _recentSearches = _recentSearches.sublist(0, 10);
    }
    
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('recent_searches', _recentSearches);
  }

  Future<void> removeRecentSearch(String query) async {
    _recentSearches.remove(query);
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('recent_searches', _recentSearches);
  }

  Future<void> searchPlaces(String query) async {
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    
    if (query.isEmpty) {
      _searchResults = [];
      notifyListeners();
      return;
    }

    _debounce = Timer(const Duration(milliseconds: 400), () async {
      _isSearching = true;
      _error = null;
      notifyListeners();

      try {
        _searchResults = await _nominatimService.searchPlaces(query);
      } catch (e) {
        _error = e.toString();
      } finally {
        _isSearching = false;
        notifyListeners();
      }
    });
  }

  Future<void> loadTrending() async {
    _isTrendingLoading = true;
    notifyListeners();

    _firestoreService.getTrendingPlaces().listen(
      (places) {
        _trendingPlaces = places;
        _isTrendingLoading = false;
        notifyListeners();
      },
      onError: (e) {
        _error = e.toString();
        _isTrendingLoading = false;
        notifyListeners();
      },
    );
  }

  Future<void> selectPlace(PlaceModel place) async {
    _selectedPlace = place;
    notifyListeners();
    // Also ensure it exists in Firestore for tracking
    await _firestoreService.upsertPlace(place);
  }

  /// For testing: Add a few mock places to Firestore
  Future<void> seedMockData() async {
    final mockPlaces = [
      PlaceModel(
        id: 'mock_1',
        name: 'Central Park',
        displayName: 'New York, NY, USA',
        category: 'park',
        description: 'An iconic urban park in the heart of Manhattan, featuring sprawling lawns, lakes, and walking paths. Perfect for a quiet afternoon escape from the city hustle.',
        latitude: 40.785091,
        longitude: -73.968285,
        crowdScore: 45,
        rating: 4.8,
        totalReviews: 1250,
        thumbnailUrl: 'https://images.unsplash.com/photo-1518235506717-e1ed3306a89b?w=600&auto=format&fit=crop&q=80',
      ),
      PlaceModel(
        id: 'mock_2',
        name: 'Eiffel Tower',
        displayName: 'Paris, France',
        category: 'tourism',
        description: 'The global cultural icon of France and one of the most recognizable structures in the world. Visitors can enjoy panoramic views of Paris from its observation decks.',
        latitude: 48.8584,
        longitude: 2.2945,
        crowdScore: 85,
        rating: 4.7,
        totalReviews: 3200,
        thumbnailUrl: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80',
      ),
      PlaceModel(
        id: 'mock_3',
        name: 'London Eye',
        displayName: 'London, UK',
        category: 'tourism',
        description: 'A giant Ferris wheel on the South Bank of the River Thames in London. It is Europe\'s tallest cantilevered observation wheel, offering stunning skyline views.',
        latitude: 51.5033,
        longitude: -0.1195,
        crowdScore: 25,
        rating: 4.6,
        totalReviews: 980,
        thumbnailUrl: 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600&auto=format&fit=crop&q=80',
      ),
    ];

    for (var place in mockPlaces) {
      await _firestoreService.upsertPlace(place);
    }
    loadTrending();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }
}
