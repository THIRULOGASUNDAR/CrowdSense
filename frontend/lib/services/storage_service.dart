import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:firebase_storage/firebase_storage.dart';
import '../core/constants/app_config.dart';

class StorageService {
  final FirebaseStorage _storage = FirebaseStorage.instance;

  Future<String> uploadCommunityPhoto(String placeId, String userId, File imageFile) async {
    final fileName = '${DateTime.now().millisecondsSinceEpoch}.jpg';
    final ref = _storage
        .ref()
        .child(AppConfig.communityPhotosPath)
        .child(placeId)
        .child(fileName);

    SettableMetadata metadata = SettableMetadata(contentType: 'image/jpeg');
    
    if (kIsWeb) {
      final bytes = await imageFile.readAsBytes();
      await ref.putData(bytes, metadata);
    } else {
      await ref.putFile(imageFile, metadata);
    }
    
    return await ref.getDownloadURL();
  }

  Future<String> uploadProfilePhoto(String userId, File imageFile) async {
    final ref = _storage
        .ref()
        .child(AppConfig.profilePhotosPath)
        .child(userId)
        .child('profile.jpg');

    SettableMetadata metadata = SettableMetadata(contentType: 'image/jpeg');

    if (kIsWeb) {
      final bytes = await imageFile.readAsBytes();
      await ref.putData(bytes, metadata);
    } else {
      await ref.putFile(imageFile, metadata);
    }
    
    return await ref.getDownloadURL();
  }

  Future<void> deletePhoto(String downloadUrl) async {
    try {
      final ref = _storage.refFromURL(downloadUrl);
      await ref.delete();
    } catch (e) {
      // Ignore if file doesn't exist
    }
  }
}
