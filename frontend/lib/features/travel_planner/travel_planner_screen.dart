import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../../providers/travel_planner_provider.dart';
import '../../providers/place_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/common/custom_button.dart';
import '../../core/utils/date_time_utils.dart';

class TravelPlannerScreen extends StatelessWidget {
  const TravelPlannerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TravelPlannerProvider>();
    final plan = provider.plan;

    return Scaffold(
      appBar: AppBar(title: const Text('Travel Planner')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Plan Your Quiet Trip', style: AppTextStyles.headlineLarge),
            const SizedBox(height: 8),
            const Text('Select source and destination to get crowd-aware travel plans.', style: AppTextStyles.bodyMedium),
            const SizedBox(height: 32),
            _buildPlaceSelector(
              context,
              label: 'From',
              place: provider.source,
              onTap: () => _pickPlace(context, (p) => provider.setSource(p)),
            ),
            const SizedBox(height: 16),
            _buildPlaceSelector(
              context,
              label: 'To',
              place: provider.destination,
              onTap: () => _pickPlace(context, (p) => provider.setDestination(p)),
            ),
            const SizedBox(height: 32),
            CustomButton(
              text: 'Calculate Best Plan',
              onPressed: (provider.source != null && provider.destination != null) ? provider.calculatePlan : null,
              isLoading: provider.isCalculating,
            ),
            if (plan != null) ...[
              const SizedBox(height: 40),
              const Text('Trip Summary', style: AppTextStyles.titleLarge),
              const SizedBox(height: 16),
              _buildPlanResult(plan),
              const SizedBox(height: 32),
              SizedBox(
                height: 250,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: FlutterMap(
                    options: MapOptions(
                      initialCenter: LatLng(plan.destinationLat, plan.destinationLng),
                      initialZoom: 13,
                    ),
                    children: [
                      TileLayer(urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'),
                      MarkerLayer(
                        markers: [
                          Marker(point: LatLng(plan.sourceLat, plan.sourceLng), child: const Icon(Icons.location_on, color: Colors.blue)),
                          Marker(point: LatLng(plan.destinationLat, plan.destinationLng), child: const Icon(Icons.location_on, color: Colors.red)),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildPlaceSelector(BuildContext context, {required String label, required dynamic place, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border),
        ),
        child: Row(
          children: [
            Icon(Icons.search_rounded, color: place != null ? AppColors.primary : AppColors.textHint),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(label, style: AppTextStyles.bodySmall),
                  Text(
                    place?.name ?? 'Select place...',
                    style: AppTextStyles.titleMedium.copyWith(color: place != null ? AppColors.textPrimary : AppColors.textHint),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlanResult(dynamic plan) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            _ResultRow(icon: Icons.straighten_rounded, label: 'Distance', value: '${plan.distanceKm.toStringAsFixed(1)} km'),
            const Divider(height: 24),
            _ResultRow(icon: Icons.timer_outlined, label: 'Estimated Time', value: DateTimeUtils.formatDuration(plan.estimatedMinutes)),
            const Divider(height: 24),
            _ResultRow(icon: Icons.access_time_filled_rounded, label: 'Recommended Visit', value: plan.recommendedVisitTime, color: AppColors.success),
          ],
        ),
      ),
    );
  }

  void _pickPlace(BuildContext context, Function(dynamic) onPick) {
    // Show a search modal or navigate to search screen in selection mode
    // For now, let's assume we use the first result from provider if searching
    context.push('/search').then((_) {
      final selected = context.read<PlaceProvider>().selectedPlace;
      if (selected != null) onPick(selected);
    });
  }
}

class _ResultRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color? color;

  const _ResultRow({required this.icon, required this.label, required this.value, this.color});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: color ?? AppColors.primary),
        const SizedBox(width: 16),
        Expanded(child: Text(label, style: AppTextStyles.bodyMedium)),
        const SizedBox(width: 8),
        Text(value, style: AppTextStyles.labelLarge.copyWith(color: color)),
      ],
    );
  }
}
