import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import '../../core/constants/app_colors.dart';

class CrowdSenseLoading extends StatelessWidget {
  final bool isFullScreen;

  const CrowdSenseLoading({super.key, this.isFullScreen = false});

  @override
  Widget build(BuildContext context) {
    if (isFullScreen) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(color: AppColors.primary),
        ),
      );
    }
    return const Center(
      child: CircularProgressIndicator(color: AppColors.primary),
    );
  }

  static Widget shimmerCard() {
    return Shimmer.fromColors(
      baseColor: Colors.grey.shade300,
      highlightColor: Colors.grey.shade100,
      child: Container(
        height: 200,
        width: double.infinity,
        margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}
