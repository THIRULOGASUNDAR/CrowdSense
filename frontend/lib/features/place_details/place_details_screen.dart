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

class _PlaceDetailsScreenState extends State<PlaceDetailsScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _contentCtrl;
  late final Animation<double> _contentFade;
  late final Animation<Offset> _contentSlide;

  @override
  void initState() {
    super.initState();
    _contentCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 600));
    _contentFade = CurvedAnimation(parent: _contentCtrl, curve: Curves.easeOut);
    _contentSlide = Tween<Offset>(begin: const Offset(0, 0.12), end: Offset.zero)
        .animate(CurvedAnimation(parent: _contentCtrl, curve: Curves.easeOut));
    _contentCtrl.forward();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CrowdProvider>().loadPrediction(widget.placeId);
    });
  }

  @override
  void dispose() {
    _contentCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final crowdProvider = context.watch<CrowdProvider>();
    final placeProvider = context.watch<PlaceProvider>();
    final favoritesProvider = context.watch<FavoritesProvider>();

    final place = placeProvider.selectedPlace;

    if (place == null) return const CrowdSenseLoading(isFullScreen: true);

    final isFav = favoritesProvider.isFavorite(place.id);

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 300,
            pinned: true,
            stretch: true,
            flexibleSpace: FlexibleSpaceBar(
              stretchModes: const [StretchMode.zoomBackground, StretchMode.fadeTitle],
              background: Stack(
                fit: StackFit.expand,
                children: [
                  CachedNetworkImage(
                    imageUrl: place.thumbnailUrl ?? '',
                    fit: BoxFit.cover,
                    placeholder: (context, url) => Container(color: AppColors.surfaceVariant),
                    errorWidget: (context, url, error) => Container(
                      color: AppColors.surfaceVariant,
                      child: const Icon(Icons.place_rounded, size: 60, color: AppColors.textHint),
                    ),
                  ),
                  // Dark gradient for readability
                  const DecoratedBox(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.bottomCenter,
                        end: Alignment.topCenter,
                        colors: [Colors.black54, Colors.transparent],
                        stops: [0, 0.6],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            actions: [
              AnimatedSwitcher(
                duration: const Duration(milliseconds: 300),
                child: IconButton(
                  key: ValueKey(isFav),
                  icon: Icon(
                    isFav ? Icons.favorite_rounded : Icons.favorite_border_rounded,
                    color: isFav ? Colors.red : Colors.white,
                  ),
                  onPressed: () async {
                    await favoritesProvider.toggleFavorite(place);
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(favoritesProvider.isFavorite(place.id)
                              ? '❤️ Added to Favorites'
                              : 'Removed from Favorites'),
                          duration: const Duration(seconds: 1),
                          behavior: SnackBarBehavior.floating,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                        ),
                      );
                    }
                  },
                ),
              ),
              IconButton(
                icon: const Icon(Icons.share_outlined, color: Colors.white),
                onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: const Text('Share link copied!'),
                    behavior: SnackBarBehavior.floating,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    duration: const Duration(seconds: 1),
                  ),
                ),
              ),
            ],
          ),
          SliverPadding(
            padding: const EdgeInsets.all(24.0),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                FadeTransition(
                  opacity: _contentFade,
                  child: SlideTransition(
                    position: _contentSlide,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(place.name, style: AppTextStyles.headlineLarge),
                                  const SizedBox(height: 4),
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: AppColors.primary.withOpacity(0.1),
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: Text(
                                      place.category ?? 'Point of Interest',
                                      style: AppTextStyles.labelLarge.copyWith(color: AppColors.primary),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
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
                        Text(place.relatedDescription, style: AppTextStyles.bodyLarge),
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
                      ],
                    ),
                  ),
                ),
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
              final barColor = score > 65 ? AppColors.crowdHigh : score > 35 ? AppColors.crowdModerate : AppColors.crowdLow;

              return Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    AnimatedContainer(
                      duration: Duration(milliseconds: 400 + index * 30),
                      curve: Curves.easeOut,
                      margin: const EdgeInsets.symmetric(horizontal: 2),
                      height: (score / 100) * 80,
                      decoration: BoxDecoration(
                        color: isCurrentHour ? barColor : barColor.withOpacity(0.35),
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
