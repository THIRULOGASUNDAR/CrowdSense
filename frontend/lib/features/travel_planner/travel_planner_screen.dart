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

class TravelPlannerScreen extends StatefulWidget {
  const TravelPlannerScreen({super.key});

  @override
  State<TravelPlannerScreen> createState() => _TravelPlannerScreenState();
}

class _TravelPlannerScreenState extends State<TravelPlannerScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _fade;
  late final Animation<Offset> _slide;
  final MapController _mapController = MapController();

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 600));
    _fade = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _slide = Tween<Offset>(begin: const Offset(0, 0.08), end: Offset.zero)
        .animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
    _ctrl.forward();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TravelPlannerProvider>();
    final plan = provider.plan;

    return Scaffold(
      appBar: AppBar(title: const Text('Travel Planner')),
      body: FadeTransition(
        opacity: _fade,
        child: SlideTransition(
          position: _slide,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [AppColors.primary.withOpacity(0.08), AppColors.accent.withOpacity(0.06)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppColors.primary.withOpacity(0.15)),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withOpacity(0.12),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(Icons.map_outlined, color: AppColors.primary, size: 28),
                      ),
                      const SizedBox(width: 16),
                      const Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Plan Your Quiet Trip', style: AppTextStyles.titleLarge),
                            SizedBox(height: 4),
                            Text(
                              'Select source and destination to get crowd-aware travel plans.',
                              style: AppTextStyles.bodySmall,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 28),
                // Source selector
                _buildPlaceSelector(
                  context,
                  label: 'From',
                  icon: Icons.trip_origin_rounded,
                  iconColor: AppColors.primary,
                  place: provider.source,
                  onTap: () => _pickPlace(context, (p) => provider.setSource(p)),
                ),
                // Arrow connector
                Center(
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 8),
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: AppColors.primary.withOpacity(0.1),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.arrow_downward_rounded, color: AppColors.primary, size: 18),
                  ),
                ),
                // Destination selector
                _buildPlaceSelector(
                  context,
                  label: 'To',
                  icon: Icons.location_on_rounded,
                  iconColor: AppColors.error,
                  place: provider.destination,
                  onTap: () => _pickPlace(context, (p) => provider.setDestination(p)),
                ),
                const SizedBox(height: 28),
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
                  // Map
                  ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: Container(
                      height: 260,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(20),
                        boxShadow: [
                          BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 16, offset: const Offset(0, 6)),
                        ],
                      ),
                      child: Stack(
                        children: [
                          FlutterMap(
                            mapController: _mapController,
                            options: MapOptions(
                              initialCameraFit: provider.routeCoordinates.isNotEmpty 
                                  ? CameraFit.bounds(
                                      bounds: LatLngBounds.fromPoints(provider.routeCoordinates),
                                      padding: const EdgeInsets.all(40),
                                    )
                                  : null,
                              initialCenter: LatLng(plan.destinationLat, plan.destinationLng),
                              initialZoom: 13,
                              interactionOptions: const InteractionOptions(
                                flags: InteractiveFlag.all,
                              ),
                            ),
                            children: [
                              TileLayer(
                                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                                userAgentPackageName: 'com.crowdsense.app',
                              ),
                              if (provider.routeCoordinates.isNotEmpty)
                                PolylineLayer(
                                  polylines: [
                                    Polyline(
                                      points: provider.routeCoordinates,
                                      color: AppColors.primary,
                                      strokeWidth: 4.0,
                                    ),
                                  ],
                                ),
                              MarkerLayer(
                                markers: [
                                  Marker(
                                    point: LatLng(plan.sourceLat, plan.sourceLng),
                                    child: Container(
                                      decoration: BoxDecoration(
                                        color: AppColors.primary,
                                        shape: BoxShape.circle,
                                        border: Border.all(color: Colors.white, width: 2),
                                      ),
                                      child: const Icon(Icons.trip_origin_rounded, color: Colors.white, size: 18),
                                    ),
                                  ),
                                  Marker(
                                    point: LatLng(plan.destinationLat, plan.destinationLng),
                                    child: Container(
                                      decoration: BoxDecoration(
                                        color: AppColors.error,
                                        shape: BoxShape.circle,
                                        border: Border.all(color: Colors.white, width: 2),
                                      ),
                                      child: const Icon(Icons.location_on_rounded, color: Colors.white, size: 18),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          Positioned(
                            right: 8,
                            top: 8,
                            child: Column(
                              children: [
                                _buildMapButton(
                                  icon: Icons.add,
                                  onTap: () {
                                    final currentZoom = _mapController.camera.zoom;
                                    _mapController.move(_mapController.camera.center, currentZoom + 1);
                                  },
                                ),
                                const SizedBox(height: 8),
                                _buildMapButton(
                                  icon: Icons.remove,
                                  onTap: () {
                                    final currentZoom = _mapController.camera.zoom;
                                    _mapController.move(_mapController.camera.center, currentZoom - 1);
                                  },
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 32),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildMapButton({required IconData icon, required VoidCallback onTap}) {
    return Material(
      color: Colors.white,
      elevation: 2,
      borderRadius: BorderRadius.circular(8),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          width: 36,
          height: 36,
          alignment: Alignment.center,
          child: Icon(icon, size: 20, color: AppColors.textPrimary),
        ),
      ),
    );
  }

  Widget _buildPlaceSelector(BuildContext context, {
    required String label,
    required IconData icon,
    required Color iconColor,
    required dynamic place,
    required VoidCallback onTap,
  }) {
    final hasPlace = place != null;
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: hasPlace ? AppColors.primary.withOpacity(0.05) : Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: hasPlace ? AppColors.primary : AppColors.border, width: hasPlace ? 1.5 : 1),
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2)),
          ],
        ),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: iconColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: iconColor, size: 22),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(label, style: AppTextStyles.bodySmall.copyWith(color: AppColors.textSecondary)),
                  Text(
                    place?.name ?? 'Tap to select place...',
                    style: AppTextStyles.titleMedium.copyWith(
                      color: hasPlace ? AppColors.textPrimary : AppColors.textHint,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
            Icon(
              hasPlace ? Icons.check_circle_rounded : Icons.arrow_forward_ios_rounded,
              color: hasPlace ? AppColors.success : AppColors.textHint,
              size: hasPlace ? 20 : 16,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlanResult(dynamic plan) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.success.withOpacity(0.06), AppColors.primary.withOpacity(0.06)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.success.withOpacity(0.2)),
      ),
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
