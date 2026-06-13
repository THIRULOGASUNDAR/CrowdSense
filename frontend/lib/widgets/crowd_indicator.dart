import 'package:flutter/material.dart';
import '../core/constants/app_colors.dart';
import '../core/constants/app_text_styles.dart';
import '../core/constants/app_config.dart';

enum CrowdIndicatorSize { small, medium, large }

class CrowdIndicator extends StatelessWidget {
  final int score;
  final CrowdIndicatorSize size;

  const CrowdIndicator({
    super.key,
    required this.score,
    this.size = CrowdIndicatorSize.medium,
  });

  Color _getColor() {
    if (score <= AppConfig.lowCrowdThreshold) return AppColors.crowdLow;
    if (score <= AppConfig.moderateCrowdThreshold) return AppColors.crowdModerate;
    return AppColors.crowdHigh;
  }

  String _getLabel() {
    if (score <= AppConfig.lowCrowdThreshold) return 'LOW';
    if (score <= AppConfig.moderateCrowdThreshold) return 'MODERATE';
    return 'HIGH';
  }

  @override
  Widget build(BuildContext context) {
    final color = _getColor();
    final label = _getLabel();

    switch (size) {
      case CrowdIndicatorSize.small:
        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            label,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
        );
      case CrowdIndicatorSize.medium:
        return Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: color, width: 1.5),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 8,
                height: 8,
                decoration: BoxDecoration(
                  color: color,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                label,
                style: AppTextStyles.labelLarge.copyWith(color: color),
              ),
            ],
          ),
        );
      case CrowdIndicatorSize.large:
        return Column(
          children: [
            Stack(
              alignment: Alignment.center,
              children: [
                SizedBox(
                  width: 120,
                  height: 120,
                  child: CircularProgressIndicator(
                    value: score / 100,
                    strokeWidth: 12,
                    backgroundColor: color.withOpacity(0.1),
                    valueColor: AlwaysStoppedAnimation<Color>(color),
                  ),
                ),
                Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      '$score%',
                      style: AppTextStyles.displayLarge.copyWith(color: color),
                    ),
                    Text(
                      label,
                      style: AppTextStyles.labelLarge.copyWith(color: color),
                    ),
                  ],
                ),
              ],
            ),
          ],
        );
    }
  }
}
