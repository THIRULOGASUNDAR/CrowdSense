import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../models/place_model.dart';
import '../core/constants/app_colors.dart';
import '../core/constants/app_text_styles.dart';
import 'crowd_indicator.dart';

class PlaceCard extends StatefulWidget {
  final PlaceModel place;
  final VoidCallback onTap;

  const PlaceCard({
    super.key,
    required this.place,
    required this.onTap,
  });

  @override
  State<PlaceCard> createState() => _PlaceCardState();
}

class _PlaceCardState extends State<PlaceCard> {
  bool _hovered = false;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _hovered = true),
      onExit: (_) => setState(() => _hovered = false),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        margin: const EdgeInsets.only(right: 4, bottom: 4, top: 2),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: _hovered
                  ? AppColors.primary.withOpacity(0.18)
                  : Colors.black.withOpacity(0.08),
              blurRadius: _hovered ? 20 : 10,
              offset: Offset(0, _hovered ? 8 : 4),
            ),
          ],
        ),
        transform: _hovered
            ? (Matrix4.identity()..translate(0.0, -3.0))
            : Matrix4.identity(),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: Material(
            color: Theme.of(context).cardTheme.color,
            child: InkWell(
              onTap: widget.onTap,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Stack(
                    children: [
                      CachedNetworkImage(
                        imageUrl: widget.place.thumbnailUrl ?? '',
                        height: 160,
                        width: double.infinity,
                        fit: BoxFit.cover,
                        placeholder: (context, url) => Container(
                          color: AppColors.surfaceVariant,
                          child: const Center(child: CircularProgressIndicator(strokeWidth: 2)),
                        ),
                        errorWidget: (context, url, error) => Container(
                          color: AppColors.surfaceVariant,
                          child: const Icon(Icons.place_rounded, color: AppColors.textHint, size: 40),
                        ),
                      ),
                      // Gradient overlay
                      Positioned(
                        bottom: 0,
                        left: 0,
                        right: 0,
                        child: Container(
                          height: 60,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              begin: Alignment.bottomCenter,
                              end: Alignment.topCenter,
                              colors: [Colors.black.withOpacity(0.5), Colors.transparent],
                            ),
                          ),
                        ),
                      ),
                      Positioned(
                        top: 10,
                        right: 10,
                        child: CrowdIndicator(
                          score: widget.place.crowdScore,
                          size: CrowdIndicatorSize.small,
                        ),
                      ),
                    ],
                  ),
                  Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.place.name,
                          style: AppTextStyles.titleMedium,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            const Icon(Icons.location_on_outlined, size: 14, color: AppColors.textSecondary),
                            const SizedBox(width: 4),
                            Expanded(
                              child: Text(
                                widget.place.displayName,
                                style: AppTextStyles.bodySmall,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          children: [
                            const Icon(Icons.star_rounded, size: 16, color: Colors.amber),
                            const SizedBox(width: 4),
                            Text(
                              widget.place.rating.toStringAsFixed(1),
                              style: AppTextStyles.labelLarge.copyWith(fontSize: 12),
                            ),
                            const SizedBox(width: 4),
                            Text(
                              '(${widget.place.totalReviews})',
                              style: AppTextStyles.bodySmall,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
