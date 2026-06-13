import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:go_router/go_router.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer(const Duration(milliseconds: 2500), _navigateToNext);
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _navigateToNext() {
    if (!mounted) return;
    
    final isLoggedIn = FirebaseAuth.instance.currentUser != null;

    if (isLoggedIn) {
      context.go('/home');
    } else {
      context.go('/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [AppColors.primary, AppColors.accent],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.radar_rounded,
              size: 100,
              color: Colors.white,
            )
            .animate()
            .fade(duration: 800.ms)
            .scale(duration: 800.ms, curve: Curves.easeOutBack),
            const SizedBox(height: 24),
            Text(
              'CrowdSense',
              style: AppTextStyles.displayLarge.copyWith(color: Colors.white),
            )
            .animate()
            .fade(delay: 400.ms, duration: 800.ms)
            .slideY(begin: 0.3, end: 0),
            const SizedBox(height: 8),
            Text(
              'Know Before You Go',
              style: AppTextStyles.titleMedium.copyWith(color: Colors.white.withOpacity(0.8)),
            )
            .animate()
            .fade(delay: 800.ms, duration: 800.ms),
          ],
        ),
      ),
    );
  }
}
