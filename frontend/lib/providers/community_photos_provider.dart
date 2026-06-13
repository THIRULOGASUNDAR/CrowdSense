import 'dart:io';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/community_photo_model.dart';
import '../services/storage_service.dart';
import '../core/constants/app_config.dart';

class CommunityPhotosProvider extends ChangeNotifier {
  final StorageService _storageService = StorageService();
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  List<CommunityPhotoModel> _photos = [];
  bool _isUploading = false;

  List<CommunityPhotoModel> get photos => _photos;
  bool get isUploading => _isUploading;

  Future<void> loadPhotos(String placeId) async {
    _db
        .collection(AppConfig.photosCollection)
        .where('placeId', isEqualTo: placeId)
        .orderBy('uploadedAt', descending: true)
        .snapshots()
        .listen((snapshot) {
      _photos = snapshot.docs.map((doc) => CommunityPhotoModel.fromFirestore(doc)).toList();
      notifyListeners();
    });
  }

  Future<void> uploadPhoto(String placeId, File imageFile, {String? caption}) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return;

    _isUploading = true;
    notifyListeners();

    try {
      final imageUrl = await _storageService.uploadCommunityPhoto(placeId, user.uid, imageFile);
      
      final photo = CommunityPhotoModel(
        id: '',
        placeId: placeId,
        userId: user.uid,
        userName: user.displayName ?? 'Anonymous',
        userPhotoUrl: user.photoURL,
        imageUrl: imageUrl,
        caption: caption,
        uploadedAt: DateTime.now(),
      );

      await _db.collection(AppConfig.photosCollection).add(photo.toMap());
      
      // Update user's uploaded photos count
      await _db.collection(AppConfig.usersCollection).doc(user.uid).update({
        'uploadedPhotos': FieldValue.arrayUnion([imageUrl]),
      });

    } catch (e) {
      debugPrint('Upload error: $e');
    } finally {
      _isUploading = false;
      notifyListeners();
    }
  }
}
