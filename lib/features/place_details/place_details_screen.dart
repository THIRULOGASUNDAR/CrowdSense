import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../providers/crowd_provider.dart';
import '../../providers/place_provider.dart';
import '../../providers/favorites_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/crowd_indicator.dart';
import '../../widgets/common/loading_widget.dart';
import '../crowd_report/crowd_report_screen.dart';

class PlaceDetailsScreen extends StatefulWidget {
  final String placeId;

  const PlaceDetailsScreen({super.key, required this.placeId});

  @override
  State<PlaceDetailsScreen> createState() => _PlaceDetailsScreenState();
}

class _PlaceDetailsScreenState extends State<PlaceDetailsScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CrowdProvider>().loadPrediction(widget.placeId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final crowdProvider = context.watch<CrowdProvider>();
    final placeProvider = context.watch<PlaceProvider>();
    final favoritesProvider = context.watch<FavoritesProvider>();
    
    // In a real app, we'd fetch the place by ID if not selected
    final place = placeProvider.selectedPlace;
    
    if (place == null) return const CrowdSenseLoading(isFullScreen: true);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 300,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: CachedNetworkImage(
                imageUrl: place.thumbnailUrl ?? 'https://picsum.photos/seed/${place.id}/800/600',
                fit: BoxFit.cover,
                placeholder: (context, url) => Container(color: Colors.grey),
              ),
            ),
            actions: [
              IconButton(
                icon: Icon(
                  favoritesProvider.isFavorite(place.id) ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                  color: favoritesProvider.isFavorite(place.id) ? Colors.red : Colors.white,
                ),
                onPressed: () async {
                  await favoritesProvider.toggleFavorite(place);
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(favoritesProvider.isFavorite(place.id) 
                          ? 'Added to Favorites' 
                          : 'Removed from Favorites'),
                        duration: const Duration(seconds: 1),
                      ),
                    );
                  }
                },
              ),
              IconButton(icon: const Icon(Icons.share_outlined, color: Colors.white), onPressed: () {}),
            ],
          ),
          SliverPadding(
            padding: const EdgeInsets.all(24.0),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(place.name, style: AppTextStyles.headlineLarge),
                          const SizedBox(height: 4),
                          Text(place.category ?? 'Point of Interest', style: AppTextStyles.labelLarge.copyWith(color: AppColors.primary)),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    const Icon(Icons.location_on_rounded, size: 18, color: AppColors.textSecondary),
                    const SizedBox(width: 8),
                    Expanded(child: Text(place.displayName, style: AppTextStyles.bodyMedium)),
                  ],
                ),
                const SizedBox(height: 32),
                _buildCrowdCard(crowdProvider),
                const SizedBox(height: 32),
                _buildForecastChart(crowdProvider),
                const SizedBox(height: 32),
                const Text('About', style: AppTextStyles.titleLarge),
                const SizedBox(height: 12),
                Text(
                  place.relatedDescription,
                  style: AppTextStyles.bodyLarge,
                ),
                const SizedBox(height: 32),
                ElevatedButton.icon(
                  onPressed: () {
                    showModalBottomSheet(
                      context: context,
                      isScrollControlled: true,
                      backgroundColor: Colors.transparent,
                      builder: (context) => CrowdReportBottomSheet(placeId: place.id),
                    );
                  },
                  icon: const Icon(Icons.report_gmailerrorred_rounded),
                  label: const Text('Report Live Crowd Level'),
                ),
                const SizedBox(height: 100),
              ]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCrowdCard(CrowdProvider provider) {
    if (provider.isLoading) {
      return const Card(child: Padding(padding: EdgeInsets.all(32), child: Center(child: CircularProgressIndicator())));
    }

    final prediction = provider.currentPrediction;
    if (prediction == null) return const SizedBox.shrink();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Row(
              children: [
                CrowdIndicator(score: prediction.score, size: CrowdIndicatorSize.large),
                const SizedBox(width: 24),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Current Status', style: AppTextStyles.titleMedium),
                      const SizedBox(height: 4),
                      Text(prediction.description, style: AppTextStyles.bodyMedium),
                    ],
                  ),
                ),
              ],
            ),
            const Divider(height: 40),
            Row(
              children: [
                const Icon(Icons.access_time_rounded, color: AppColors.primary),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Best Time to Visit', style: AppTextStyles.labelLarge),
                      Text(prediction.bestTimeToVisit, style: AppTextStyles.bodyLarge.copyWith(fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildForecastChart(CrowdProvider provider) {
    if (provider.isLoading || provider.hourlyForecast.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Crowd Forecast', style: AppTextStyles.titleLarge),
        const SizedBox(height: 16),
        Container(
          height: 150,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 20),
          decoration: BoxDecoration(
            color: AppColors.surface,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.border),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: List.generate(provider.hourlyForecast.length, (index) {
              final score = provider.hourlyForecast[index];
              final hour = index + 6; // Starts at 6 AM
              final isCurrentHour = DateTime.now().hour == hour;

              return Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Container(
                      margin: const EdgeInsets.symmetric(horizontal: 2),
                      height: (score / 100) * 80,
                      decoration: BoxDecoration(
                        color: isCurrentHour ? AppColors.primary : AppColors.primary.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(4),
                      ),
                    ),
                    const SizedBox(height: 8),
                    if (hour % 4 == 0)
                      Text(
                        hour > 12 ? '${hour - 12}p' : '$hour${hour == 12 ? 'p' : 'a'}',
                        style: AppTextStyles.bodySmall.copyWith(fontSize: 9),
                      )
                    else
                      const SizedBox(height: 12),
                  ],
                ),
              );
            }),
          ),
        ),
      ],
    );
  }
}
