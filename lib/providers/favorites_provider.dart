import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/place_model.dart';
import '../services/firestore_service.dart';

class FavoritesProvider extends ChangeNotifier {
  final FirestoreService _firestoreService = FirestoreService();
  List<String> _favoriteIds = [];
  List<PlaceModel> _favorites = [];

  List<PlaceModel> get favorites => _favorites;
  
  FavoritesProvider() {
    _init();
  }

  void _init() {
    FirebaseAuth.instance.authStateChanges().listen((user) {
      if (user != null) {
        _firestoreService.getFavoritePlaceIds(user.uid).listen((ids) async {
          _favoriteIds = ids;
          
          final List<PlaceModel> fetchedPlaces = [];
          for (final id in ids) {
            try {
              final place = await _firestoreService.getPlace(id);
              if (place != null) {
                fetchedPlaces.add(place);
              }
            } catch (e) {
              debugPrint('Error fetching favorite place $id: $e');
            }
          }
          _favorites = fetchedPlaces;
          notifyListeners();
        });
      } else {
        _favoriteIds = [];
        _favorites = [];
        notifyListeners();
      }
    });
  }

  bool isFavorite(String placeId) => _favoriteIds.contains(placeId);

  Future<void> toggleFavorite(PlaceModel place) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    if (isFavorite(place.id)) {
      _favoriteIds.remove(place.id);
      _favorites.removeWhere((p) => p.id == place.id);
      notifyListeners();
      await _firestoreService.removeFavorite(user.uid, place.id);
    } else {
      _favoriteIds.add(place.id);
      _favorites.add(place);
      notifyListeners();

      // Ensure place is in Firestore
      await _firestoreService.upsertPlace(place);
      await _firestoreService.addFavorite(user.uid, place.id);
    }
  }
}
