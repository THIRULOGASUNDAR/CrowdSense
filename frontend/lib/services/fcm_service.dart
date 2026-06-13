import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import '../core/constants/app_config.dart';

class FCMService {
  final FirebaseMessaging _fcm = FirebaseMessaging.instance;

  Future<void> initialize() async {
    // Basic initialization for foreground messaging
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      debugPrint("Foreground message received: ${message.notification?.title}");
    });

    // Request permission (Mobile/Web)
    NotificationSettings settings = await _fcm.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      // Small delay on Web to allow Service Worker activation
      if (kIsWeb) {
        await Future.delayed(const Duration(seconds: 3));
      }

      try {
        // Attempt to get token - on Web this requires the service worker to be ready
        String? token = await _fcm.getToken(
          vapidKey: "BPnknwgTNh-tGdbzjJK9J0aVMYKOwVlrgaS-O01h78CQQUKKXJ80TRgN414GuyWnoAuSlZSxNQKn-Xsl8zG8wzk"
        );
        if (token != null) {
          await _saveTokenToFirestore(token);
        }
      } catch (e) {
        debugPrint('FCM Token generation failed: $e. This is common on Web if the service worker isn\'t active yet.');
      }
    }
  }

  Future<void> _saveTokenToFirestore(String token) async {
    final user = FirebaseAuth.instance.currentUser;
    if (user != null) {
      await FirebaseFirestore.instance
          .collection(AppConfig.usersCollection)
          .doc(user.uid)
          .set({
        'fcmToken': token,
        'updatedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
    }
  }

  Future<void> subscribeToTopic(String topic) async {
    await _fcm.subscribeToTopic(topic);
  }

  static Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
    // Handle background message
  }
}
