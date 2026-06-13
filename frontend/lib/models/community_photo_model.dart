import 'package:cloud_firestore/cloud_firestore.dart';

class CommunityPhotoModel {
  final String id;
  final String placeId;
  final String userId;
  final String userName;
  final String? userPhotoUrl;
  final String imageUrl;
  final String? caption;
  final int likes;
  final DateTime uploadedAt;

  const CommunityPhotoModel({
    required this.id,
    required this.placeId,
    required this.userId,
    required this.userName,
    this.userPhotoUrl,
    required this.imageUrl,
    this.caption,
    this.likes = 0,
    required this.uploadedAt,
  });

  factory CommunityPhotoModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return CommunityPhotoModel(
      id: doc.id,
      placeId: data['placeId'] ?? '',
      userId: data['userId'] ?? '',
      userName: data['userName'] ?? 'Anonymous',
      userPhotoUrl: data['userPhotoUrl'],
      imageUrl: data['imageUrl'] ?? '',
      caption: data['caption'],
      likes: data['likes'] ?? 0,
      uploadedAt: (data['uploadedAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toMap() => {
    'placeId': placeId,
    'userId': userId,
    'userName': userName,
    'userPhotoUrl': userPhotoUrl,
    'imageUrl': imageUrl,
    'caption': caption,
    'likes': likes,
    'uploadedAt': FieldValue.serverTimestamp(),
  };
}
