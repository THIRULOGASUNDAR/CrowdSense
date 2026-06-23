import 'dart:io';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/user_model.dart';
import '../services/firestore_service.dart';
import '../services/storage_service.dart';

class ProfileProvider extends ChangeNotifier {
  final FirestoreService _firestoreService = FirestoreService();
  final StorageService _storageService = StorageService();
  UserModel? _userProfile;
  bool _isLoading = false;
  StreamSubscription<UserModel?>? _profileSubscription;

  UserModel? get userProfile => _userProfile;
  bool get isLoading => _isLoading;

  ProfileProvider() {
    FirebaseAuth.instance.authStateChanges().listen((user) {
      if (user != null) {
        loadProfile(user.uid);
      } else {
        _profileSubscription?.cancel();
        _userProfile = null;
        notifyListeners();
      }
    });
  }

  void loadProfile(String uid) {
    _isLoading = true;
    notifyListeners();
    
    _profileSubscription?.cancel();
    _profileSubscription = _firestoreService.getUserStream(uid).listen(
      (profile) {
        _userProfile = profile;
        _isLoading = false;
        notifyListeners();
      },
      onError: (e) {
        debugPrint('Error loading profile stream: $e');
        _isLoading = false;
        notifyListeners();
      }
    );
  }

  @override
  void dispose() {
    _profileSubscription?.cancel();
    super.dispose();
  }

  Future<void> updateDisplayName(String name) async {
    if (_userProfile == null) return;
    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user != null) {
        await user.updateDisplayName(name);
      }
      final updated = _userProfile!.copyWith(displayName: name);
      await _firestoreService.updateUser(updated);
      _userProfile = updated;
      notifyListeners();
    } catch (e) {
      debugPrint('Error updating name: $e');
    }
  }

  Future<void> updateProfileDetails(String name, String phone, String bio) async {
    if (_userProfile == null) return;
    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user != null) {
        await user.updateDisplayName(name);
      }
      final updated = _userProfile!.copyWith(
        displayName: name,
        phone: phone,
        bio: bio,
      );
      await _firestoreService.updateUser(updated);
      _userProfile = updated;
      notifyListeners();
    } catch (e) {
      debugPrint('Error updating profile details: $e');
    }
  }

  Future<void> updateProfilePhoto(File imageFile) async {
    if (_userProfile == null) return;
    _isLoading = true;
    notifyListeners();

    try {
      final photoUrl = await _storageService.uploadProfilePhoto(_userProfile!.uid, imageFile);
      
      final user = FirebaseAuth.instance.currentUser;
      if (user != null) {
        await user.updatePhotoURL(photoUrl);
      }

      final updated = _userProfile!.copyWith(photoUrl: photoUrl);
      await _firestoreService.updateUser(updated);
      _userProfile = updated;
    } catch (e) {
      debugPrint('Error updating photo: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
