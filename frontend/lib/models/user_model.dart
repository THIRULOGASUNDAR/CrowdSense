import 'package:cloud_firestore/cloud_firestore.dart';

class UserModel {
  final String uid;
  final String email;
  final String displayName;
  final String? photoUrl;
  final List<String> uploadedPhotos;
  final List<String> savedPlaces;
  final int totalReports;
  final DateTime joinedAt;
  final String? phone;
  final String? bio;

  const UserModel({
    required this.uid,
    required this.email,
    required this.displayName,
    this.photoUrl,
    this.uploadedPhotos = const [],
    this.savedPlaces = const [],
    this.totalReports = 0,
    required this.joinedAt,
    this.phone,
    this.bio,
  });

  factory UserModel.fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;
    return UserModel(
      uid: doc.id,
      email: data['email'] ?? '',
      displayName: data['displayName'] ?? '',
      photoUrl: data['photoUrl'],
      uploadedPhotos: List<String>.from(data['uploadedPhotos'] ?? []),
      savedPlaces: List<String>.from(data['savedPlaces'] ?? []),
      totalReports: data['totalReports'] ?? 0,
      joinedAt: (data['joinedAt'] as Timestamp?)?.toDate() ?? DateTime.now(),
      phone: data['phone'],
      bio: data['bio'],
    );
  }

  Map<String, dynamic> toMap() => {
    'email': email,
    'displayName': displayName,
    'photoUrl': photoUrl,
    'uploadedPhotos': uploadedPhotos,
    'savedPlaces': savedPlaces,
    'totalReports': totalReports,
    'joinedAt': joinedAt,
    'phone': phone,
    'bio': bio,
  };

  UserModel copyWith({
    String? displayName,
    String? photoUrl,
    List<String>? uploadedPhotos,
    List<String>? savedPlaces,
    int? totalReports,
    String? phone,
    String? bio,
  }) {
    return UserModel(
      uid: uid,
      email: email,
      displayName: displayName ?? this.displayName,
      photoUrl: photoUrl ?? this.photoUrl,
      uploadedPhotos: uploadedPhotos ?? this.uploadedPhotos,
      savedPlaces: savedPlaces ?? this.savedPlaces,
      totalReports: totalReports ?? this.totalReports,
      joinedAt: joinedAt,
      phone: phone ?? this.phone,
      bio: bio ?? this.bio,
    );
  }
}
