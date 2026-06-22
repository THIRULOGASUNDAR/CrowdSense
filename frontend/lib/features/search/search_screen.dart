import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../providers/place_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/common/loading_widget.dart';
import '../../widgets/common/empty_state_widget.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> with SingleTickerProviderStateMixin {
  final _searchController = TextEditingController();
  late final AnimationController _listAnimCtrl;

  @override
  void initState() {
    super.initState();
    _listAnimCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 400));
    _searchController.addListener(() => setState(() {}));
  }

  @override
  void dispose() {
    _searchController.dispose();
    _listAnimCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<PlaceProvider>();
    final results = provider.searchResults;

    // Trigger list animation when results arrive
    if (results.isNotEmpty && !_listAnimCtrl.isAnimating && _listAnimCtrl.value == 0) {
      _listAnimCtrl.forward(from: 0);
    }

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 0,
        title: Padding(
          padding: const EdgeInsets.only(right: 16.0),
          child: TextField(
            controller: _searchController,
            autofocus: true,
            onChanged: (value) {
              provider.searchPlaces(value);
              if (value.isNotEmpty) _listAnimCtrl.forward(from: 0);
            },
            decoration: InputDecoration(
              hintText: 'Search for places...',
              prefixIcon: const Icon(Icons.search_rounded),
              suffixIcon: _searchController.text.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.close_rounded),
                      onPressed: () {
                        _searchController.clear();
                        provider.searchPlaces('');
                      },
                    )
                  : null,
              contentPadding: const EdgeInsets.symmetric(vertical: 12),
              fillColor: AppColors.surfaceVariant,
              filled: true,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
            ),
          ),
        ),
      ),
      body: provider.isSearching
          ? const CrowdSenseLoading()
          : results.isEmpty && _searchController.text.isNotEmpty
              ? EmptyStateWidget.noResults()
              : results.isEmpty
                  ? _buildInitialState()
                  : ListView.separated(
                      padding: const EdgeInsets.all(16),
                      itemCount: results.length,
                      separatorBuilder: (_, __) => const Divider(height: 1),
                      itemBuilder: (context, index) {
                        final place = results[index];
                        return AnimatedBuilder(
                          animation: _listAnimCtrl,
                          builder: (context, child) {
                            final delay = (index * 0.08).clamp(0.0, 0.6);
                            final start = delay;
                            final end = (delay + 0.4).clamp(0.0, 1.0);
                            final anim = CurvedAnimation(
                              parent: _listAnimCtrl,
                              curve: Interval(start, end, curve: Curves.easeOut),
                            );
                            return FadeTransition(
                              opacity: anim,
                              child: SlideTransition(
                                position: Tween<Offset>(
                                  begin: const Offset(0.05, 0),
                                  end: Offset.zero,
                                ).animate(anim),
                                child: child,
                              ),
                            );
                          },
                          child: ListTile(
                            leading: Container(
                              width: 40,
                              height: 40,
                              decoration: BoxDecoration(
                                color: AppColors.primary.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(10),
                              ),
                              child: const Icon(Icons.place_outlined, color: AppColors.primary, size: 20),
                            ),
                            title: Text(place.name, style: AppTextStyles.titleMedium),
                            subtitle: Text(place.displayName, maxLines: 1, overflow: TextOverflow.ellipsis),
                            trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 14, color: AppColors.textHint),
                            onTap: () {
                              provider.addRecentSearch(place.name);
                              provider.selectPlace(place);
                              context.push('/place/${place.id}');
                            },
                          ),
                        );
                      },
                    ),
    );
  }

  Widget _buildInitialState() {
    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Quick Searches', style: AppTextStyles.titleMedium),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _SuggestionChip(label: 'Coffee Shop'),
              _SuggestionChip(label: 'Library'),
              _SuggestionChip(label: 'Shopping Mall'),
              _SuggestionChip(label: 'Museum'),
              _SuggestionChip(label: 'Park'),
              _SuggestionChip(label: 'Restaurant'),
            ],
          ),
        ],
      ),
    );
  }
}

class _SuggestionChip extends StatelessWidget {
  final String label;

  const _SuggestionChip({required this.label});

  @override
  Widget build(BuildContext context) {
    final provider = context.read<PlaceProvider>();
    return ActionChip(
      label: Text(label),
      avatar: const Icon(Icons.search_rounded, size: 16),
      onPressed: () {
        provider.searchPlaces(label);
      },
      backgroundColor: AppColors.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10), side: const BorderSide(color: AppColors.border)),
    );
  }
}
