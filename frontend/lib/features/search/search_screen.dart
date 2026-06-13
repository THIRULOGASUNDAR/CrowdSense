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

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<PlaceProvider>();
    final results = provider.searchResults;

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 0,
        title: Padding(
          padding: const EdgeInsets.only(right: 16.0),
          child: TextField(
            controller: _searchController,
            autofocus: true,
            onChanged: (value) => provider.searchPlaces(value),
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
                        return ListTile(
                          leading: const Icon(Icons.place_outlined, color: AppColors.primary),
                          title: Text(place.name, style: AppTextStyles.titleMedium),
                          subtitle: Text(place.displayName, maxLines: 1, overflow: TextOverflow.ellipsis),
                          onTap: () {
                            provider.addRecentSearch(place.name);
                            provider.selectPlace(place);
                            context.push('/place/${place.id}');
                          },
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
          const Text('Recent Searches', style: AppTextStyles.titleMedium),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            children: [
              _SuggestionChip(label: 'Coffee Shop'),
              _SuggestionChip(label: 'Library'),
              _SuggestionChip(label: 'Shopping Mall'),
              _SuggestionChip(label: 'Museum'),
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
    return ActionChip(
      label: Text(label),
      onPressed: () {},
      backgroundColor: AppColors.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8), side: const BorderSide(color: AppColors.border)),
    );
  }
}
