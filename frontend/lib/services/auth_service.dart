import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../core/constants/app_config.dart';
import '../core/errors/app_exceptions.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  User? get currentUser => _auth.currentUser;

  Future<UserCredential> signInWithEmailAndPassword(String email, String password) async {
    try {
      return await _auth.signInWithEmailAndPassword(email: email, password: password);
    } on FirebaseAuthException catch (e) {
      throw AppException(_handleAuthError(e));
    } catch (e) {
      throw AppException('An unexpected error occurred during sign in.');
    }
  }

  Future<UserCredential> createUserWithEmailAndPassword(
      String email, String password, String displayName) async {
    try {
      final credential = await _auth.createUserWithEmailAndPassword(email: email, password: password);
      
      if (credential.user != null) {
        await credential.user!.updateDisplayName(displayName);
        
        // Create user document in Firestore
        await _firestore.collection(AppConfig.usersCollection).doc(credential.user!.uid).set({
          'email': email,
          'displayName': displayName,
          'joinedAt': FieldValue.serverTimestamp(),
          'uploadedPhotos': [],
          'savedPlaces': [],
          'totalReports': 0,
        });
      }
      
      return credential;
    } on FirebaseAuthException catch (e) {
      throw AppException(_handleAuthError(e));
    } catch (e) {
      throw AppException('An unexpected error occurred during registration.');
    }
  }

  Future<void> sendPasswordResetEmail(String email) async {
    try {
      await _auth.sendPasswordResetEmail(email: email);
    } on FirebaseAuthException catch (e) {
      throw AppException(_handleAuthError(e));
    } catch (e) {
      throw AppException('An unexpected error occurred while sending reset email.');
    }
  }

  Future<void> signOut() async {
    await _auth.signOut();
  }

  String _handleAuthError(FirebaseAuthException e) {
    switch (e.code) {
      case 'user-not-found':
        return 'No user found for that email.';
      case 'wrong-password':
        return 'Wrong password provided for that user.';
      case 'email-already-in-use':
        return 'The account already exists for that email.';
      case 'invalid-email':
        return 'The email address is not valid.';
      case 'weak-password':
        return 'The password provided is too weak.';
      default:
        return e.message ?? 'Authentication failed.';
    }
  }
}
