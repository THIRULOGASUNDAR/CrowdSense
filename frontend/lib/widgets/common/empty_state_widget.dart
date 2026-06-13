import 'package:flutter/material.dart';
import '../../core/constants/app_text_styles.dart';
import '../../core/constants/app_colors.dart';
import 'custom_button.dart';

class EmptyStateWidget extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onAction;

  const EmptyStateWidget({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onAction,
  });

  factory EmptyStateWidget.noResults() {
    return const EmptyStateWidget(
      icon: Icons.search_off_rounded,
      title: 'No results found',
      subtitle: 'Try searching for something else.',
    );
  }

  factory EmptyStateWidget.noFavorites() {
    return const EmptyStateWidget(
      icon: Icons.favorite_border_rounded,
      title: 'No favorites yet',
      subtitle: 'Save places to view them here later.',
    );
  }

  factory EmptyStateWidget.noPhotos() {
    return const EmptyStateWidget(
      icon: Icons.add_a_photo_outlined,
      title: 'No photos yet',
      subtitle: 'Be the first to upload a photo of this place!',
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 80, color: AppColors.textHint),
            const SizedBox(height: 24),
            Text(
              title,
              style: AppTextStyles.headlineMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            Text(
              subtitle,
              style: AppTextStyles.bodyMedium,
              textAlign: TextAlign.center,
            ),
            if (actionLabel != null && onAction != null) ...[
              const SizedBox(height: 32),
              CustomButton(
                text: actionLabel!,
                onPressed: onAction!,
                variant: ButtonVariant.outline,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
