import 'package:cloud_firestore/cloud_firestore.dart';

enum CrowdReportLevel { low, moderate, high }

extension CrowdReportLevelExt on CrowdReportLevel {
  String get label {
    switch (this) {
      case CrowdReportLevel.low:      return 'Low';
      case CrowdReportLevel.moderate: return 'Moderate';
      case CrowdReportLevel.high:     return 'High';
    }
  }
  int get score {
    switch (this) {
      case CrowdReportLevel.low:      return 20;
      case CrowdReportLevel.moderate: return 55;
      case CrowdReportLevel.high:     return 85;
    }
  }
}

class CrowdReportModel {
  final String id;
  final String placeId;
  final String userId;
  final String userName;
  final CrowdReportLevel level;
  final String? note;
  final DateTime reportedAt;

  const CrowdReportModel({
    required this.id,
    required this.placeId,
    required this.userId,
    required this.userName,
    required this.level,
    this.note,
    required this.reportedAt,
  });

  factory CrowdReportModel.fromFirestore(DocumentSnapshot doc) {
    final d = doc.data() as Map<String, dynamic>;
    return CrowdReportModel(
      id:         doc.id,
      placeId:    d['placeId'] ?? '',
      userId:     d['userId'] ?? '',
      userName:   d['userName'] ?? 'Anonymous',
      level:      CrowdReportLevel.values.firstWhere(
        (e) => e.name == d['level'],
        orElse: () => CrowdReportLevel.moderate,
      ),
      note:       d['note'],
      reportedAt: (d['reportedAt'] as Timestamp).toDate(),
    );
  }

  Map<String, dynamic> toMap() => {
    'placeId':    placeId,
    'userId':     userId,
    'userName':   userName,
    'level':      level.name,
    'score':      level.score,
    'note':       note,
    'reportedAt': FieldValue.serverTimestamp(),
  };
}
