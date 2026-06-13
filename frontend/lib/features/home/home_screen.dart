import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';
import '../../providers/place_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/place_card.dart';
import '../../widgets/common/loading_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PlaceProvider>().loadTrending();
    });
  }

  void _searchCategory(BuildContext context, String category) {
    context.read<PlaceProvider>().searchPlaces(category);
    context.go('/search-results');
  }

  @override
  Widget build(BuildContext context) {
    final user = context.watch<AuthProvider>().currentUser;
    final provider = context.watch<PlaceProvider>();
    final trending = provider.trendingPlaces;
    final isLoading = provider.isTrendingLoading;
    final error = provider.error;

    return Scaffold(
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: () async => provider.loadTrending(),
          child: CustomScrollView(
            slivers: [
              if (error != null)
                SliverToBoxAdapter(
                  child: Container(
                    color: AppColors.error.withOpacity(0.1),
                    padding: const EdgeInsets.all(16),
                    child: Text('Error loading data: $error', style: TextStyle(color: AppColors.error)),
                  ),
                ),
              SliverPadding(
                padding: const EdgeInsets.all(24.0),
                sliver: SliverToBoxAdapter(
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
                                Text(
                                  'Good morning, ${user?.displayName?.split(' ').first ?? 'Adventurer'}!',
                                  style: AppTextStyles.headlineLarge,
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                                const Text(
                                  'Where are you heading today?',
                                  style: AppTextStyles.bodyMedium,
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 16),
                          GestureDetector(
                            onTap: () => context.go('/profile'),
                            child: CircleAvatar(
                              radius: 24,
                              backgroundColor: AppColors.primaryLight,
                              backgroundImage: user?.photoURL != null ? NetworkImage(user!.photoURL!) : null,
                              child: user?.photoURL == null ? const Icon(Icons.person, color: Colors.white) : null,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 32),
                      GestureDetector(
                        onTap: () => context.go('/search'),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(16),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.05),
                                blurRadius: 10,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.search_rounded, color: AppColors.primary),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  'Search places, parks, restaurants...',
                                  style: AppTextStyles.bodyMedium.copyWith(color: AppColors.textHint),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              const SizedBox(width: 12),
                              const Icon(Icons.mic_none_rounded, color: AppColors.textHint),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 32),
                      _SectionHeader(title: 'Trending Now', onSeeAll: () {}),
                    ],
                  ),
                ),
              ),
              SliverToBoxAdapter(
                child: isLoading
                    ? SizedBox(
                        height: 250,
                        child: ListView.builder(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          itemCount: 3,
                          itemBuilder: (_, __) => SizedBox(width: 280, child: CrowdSenseLoading.shimmerCard()),
                        ),
                      )
                    : trending.isEmpty
                        ? Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 24.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('No trending places yet. Start searching to discover new spots!', style: AppTextStyles.bodyMedium),
                                const SizedBox(height: 12),
                                TextButton.icon(
                                  onPressed: () => provider.seedMockData(),
                                  icon: const Icon(Icons.auto_awesome),
                                  label: const Text('Seed Sample Data'),
                                ),
                              ],
                            ),
                          )
                        : SizedBox(
                            height: 280,
                            child: ListView.builder(
                              scrollDirection: Axis.horizontal,
                              padding: const EdgeInsets.symmetric(horizontal: 16),
                              itemCount: trending.length,
                              itemBuilder: (context, index) {
                                final place = trending[index];
                                return SizedBox(
                                  width: 280,
                                  child: PlaceCard(
                                    place: place,
                                    onTap: () {
                                      provider.selectPlace(place);
                                      context.push('/place/${place.id}');
                                    },
                                  ),
                                );
                              },
                            ),
                          ),
              ),
              SliverPadding(
                padding: const EdgeInsets.all(24.0),
                sliver: SliverToBoxAdapter(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const _SectionHeader(title: 'Popular Categories'),
                      const SizedBox(height: 16),
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: [
                            _CategoryChip(
                              label: 'Landmarks', 
                              icon: '🏛️',
                              onTap: () => _searchCategory(context, 'Landmarks'),
                            ),
                            _CategoryChip(
                              label: 'Restaurants', 
                              icon: '🍽️',
                              onTap: () => _searchCategory(context, 'Restaurants'),
                            ),
                            _CategoryChip(
                              label: 'Parks', 
                              icon: '🌳',
                              onTap: () => _searchCategory(context, 'Parks'),
                            ),
                            _CategoryChip(
                              label: 'Shopping', 
                              icon: '🛍️',
                              onTap: () => _searchCategory(context, 'Shopping'),
                            ),
                            _CategoryChip(
                              label: 'Entertainment', 
                              icon: '🎭',
                              onTap: () => _searchCategory(context, 'Entertainment'),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 32),
                      const _SectionHeader(title: 'Recent Searches'),
                      const SizedBox(height: 16),
                      provider.recentSearches.isEmpty
                          ? Text('Your recent searches will appear here.', style: AppTextStyles.bodySmall)
                          : Wrap(
                              spacing: 8,
                              children: provider.recentSearches.map((query) => _RecentSearchChip(
                                label: query,
                                onDelete: () => provider.removeRecentSearch(query),
                                onTap: () {
                                  context.go('/search');
                                  // Optionally pre-fill the search
                                },
                              )).toList(),
                            ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final VoidCallback? onSeeAll;

  const _SectionHeader({required this.title, this.onSeeAll});

  void _searchCategory(BuildContext context, String category) {
    context.read<PlaceProvider>().searchPlaces(category);
    context.go('/search-results');
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(child: Text(title, style: AppTextStyles.titleLarge, overflow: TextOverflow.ellipsis)),
        if (onSeeAll != null)
          TextButton(
            onPressed: onSeeAll,
            child: const Text('See All'),
          ),
      ],
    );
  }
}

class _CategoryChip extends StatelessWidget {
  final String label;
  final String icon;
  final VoidCallback onTap;

  const _CategoryChip({required this.label, required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(right: 12),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border),
        ),
        child: Row(
          children: [
            Text(icon, style: const TextStyle(fontSize: 18)),
            const SizedBox(width: 8),
            Text(label, style: AppTextStyles.labelLarge),
          ],
        ),
      ),
    );
  }
}

class _RecentSearchChip extends StatelessWidget {
  final String label;
  final VoidCallback onDelete;
  final VoidCallback onTap;

  const _RecentSearchChip({required this.label, required this.onDelete, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InputChip(
      label: Text(label),
      backgroundColor: AppColors.surfaceVariant,
      onPressed: onTap,
      onDeleted: onDelete,
      deleteIcon: const Icon(Icons.close, size: 14),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8), side: BorderSide.none),
    );
  }
}
