import 'package:flutter/material.dart';

/// CrowdSense brand colour palette — Material 3 compatible.
class AppColors {
  AppColors._();

  // Primary brand
  static const Color primary        = Color(0xFF2563EB);
  static const Color primaryLight   = Color(0xFF60A5FA);
  static const Color primaryDark    = Color(0xFF1E40AF);

  // Accent
  static const Color accent         = Color(0xFF7C3AED);
  static const Color accentLight    = Color(0xFFA78BFA);

  // Semantic
  static const Color success        = Color(0xFF10B981);
  static const Color warning        = Color(0xFFF59E0B);
  static const Color error          = Color(0xFFEF4444);

  // Crowd level colours
  static const Color crowdLow       = Color(0xFF10B981);
  static const Color crowdModerate  = Color(0xFFF59E0B);
  static const Color crowdHigh      = Color(0xFFEF4444);

  // Neutrals
  static const Color background     = Color(0xFFF8FAFC);
  static const Color surface        = Color(0xFFFFFFFF);
  static const Color surfaceVariant = Color(0xFFF1F5F9);
  static const Color border         = Color(0xFFE2E8F0);
  static const Color textPrimary    = Color(0xFF0F172A);
  static const Color textSecondary  = Color(0xFF64748B);
  static const Color textHint       = Color(0xFF94A3B8);

  // Dark mode
  static const Color darkBackground    = Color(0xFF0F172A);
  static const Color darkSurface       = Color(0xFF1E293B);
  static const Color darkSurfaceVariant= Color(0xFF334155);
  static const Color darkTextPrimary   = Color(0xFFF8FAFC);
  static const Color darkTextSecondary = Color(0xFF94A3B8);
}
