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

class _HomeScreenState extends State<HomeScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _headerController;
  late final Animation<double> _headerFade;
  late final Animation<Offset> _headerSlide;

  @override
  void initState() {
    super.initState();
    _headerController = AnimationController(vsync: this, duration: const Duration(milliseconds: 700));
    _headerFade = CurvedAnimation(parent: _headerController, curve: Curves.easeOut);
    _headerSlide = Tween<Offset>(begin: const Offset(0, -0.1), end: Offset.zero)
        .animate(CurvedAnimation(parent: _headerController, curve: Curves.easeOut));
    _headerController.forward();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PlaceProvider>().loadTrending();
    });
  }

  @override
  void dispose() {
    _headerController.dispose();
    super.dispose();
  }

  void _searchCategory(BuildContext context, String category) {
    context.read<PlaceProvider>().searchPlaces(category);
    context.go('/search-results');
  }

  String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
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
              // Gradient header
              SliverToBoxAdapter(
                child: FadeTransition(
                  opacity: _headerFade,
                  child: SlideTransition(
                    position: _headerSlide,
                    child: Container(
                      padding: const EdgeInsets.fromLTRB(24, 24, 24, 32),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [AppColors.primary, AppColors.accent],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                        borderRadius: const BorderRadius.only(
                          bottomLeft: Radius.circular(28),
                          bottomRight: Radius.circular(28),
                        ),
                      ),
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
                                      '${_getGreeting()}, ${user?.displayName?.split(' ').first ?? 'Adventurer'}! 👋',
                                      style: AppTextStyles.headlineLarge.copyWith(color: Colors.white),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      'Where are you heading today?',
                                      style: AppTextStyles.bodyMedium.copyWith(color: Colors.white70),
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(width: 16),
                              GestureDetector(
                                onTap: () => context.go('/profile'),
                                child: Hero(
                                  tag: 'profile_avatar',
                                  child: Container(
                                    width: 48,
                                    height: 48,
                                    decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      color: Colors.white.withOpacity(0.25),
                                      border: Border.all(color: Colors.white, width: 2),
                                    ),
                                    child: Center(
                                      child: Text(
                                        (user?.displayName != null && user!.displayName!.isNotEmpty)
                                            ? user.displayName![0].toUpperCase()
                                            : 'A',
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 18,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 24),
                          // Search bar
                          GestureDetector(
                            onTap: () => context.go('/search'),
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(16),
                                boxShadow: [
                                  BoxShadow(
                                    color: Colors.black.withOpacity(0.1),
                                    blurRadius: 12,
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
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
              // Trending now
              SliverPadding(
                padding: const EdgeInsets.fromLTRB(24, 28, 24, 0),
                sliver: SliverToBoxAdapter(
                  child: _SectionHeader(title: 'Trending Now 🔥', onSeeAll: () {}),
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
                            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16),
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
                              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                              itemCount: trending.length,
                              itemBuilder: (context, index) {
                                final place = trending[index];
                                return _AnimatedCard(
                                  delay: index * 80,
                                  child: SizedBox(
                                    width: 280,
                                    child: PlaceCard(
                                      place: place,
                                      onTap: () {
                                        provider.selectPlace(place);
                                        context.push('/place/${place.id}');
                                      },
                                    ),
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
                            _CategoryChip(label: 'Landmarks', icon: '🏛️', onTap: () => _searchCategory(context, 'Landmarks')),
                            _CategoryChip(label: 'Restaurants', icon: '🍽️', onTap: () => _searchCategory(context, 'Restaurants')),
                            _CategoryChip(label: 'Parks', icon: '🌳', onTap: () => _searchCategory(context, 'Parks')),
                            _CategoryChip(label: 'Shopping', icon: '🛍️', onTap: () => _searchCategory(context, 'Shopping')),
                            _CategoryChip(label: 'Entertainment', icon: '🎭', onTap: () => _searchCategory(context, 'Entertainment')),
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
                              runSpacing: 8,
                              children: provider.recentSearches.map((query) => _RecentSearchChip(
                                label: query,
                                onDelete: () => provider.removeRecentSearch(query),
                                onTap: () {
                                  context.go('/search');
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

class _AnimatedCard extends StatefulWidget {
  final int delay;
  final Widget child;

  const _AnimatedCard({required this.delay, required this.child});

  @override
  State<_AnimatedCard> createState() => _AnimatedCardState();
}

class _AnimatedCardState extends State<_AnimatedCard> with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _fade;
  late final Animation<Offset> _slide;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 500));
    _fade = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _slide = Tween<Offset>(begin: const Offset(0, 0.15), end: Offset.zero)
        .animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
    Future.delayed(Duration(milliseconds: widget.delay), () {
      if (mounted) _ctrl.forward();
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _fade,
      child: SlideTransition(position: _slide, child: widget.child),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final VoidCallback? onSeeAll;

  const _SectionHeader({required this.title, this.onSeeAll});

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

class _CategoryChip extends StatefulWidget {
  final String label;
  final String icon;
  final VoidCallback onTap;

  const _CategoryChip({required this.label, required this.icon, required this.onTap});

  @override
  State<_CategoryChip> createState() => _CategoryChipState();
}

class _CategoryChipState extends State<_CategoryChip> {
  bool _pressed = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _pressed = true),
      onTapUp: (_) {
        setState(() => _pressed = false);
        widget.onTap();
      },
      onTapCancel: () => setState(() => _pressed = false),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        margin: const EdgeInsets.only(right: 12),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        transform: _pressed ? (Matrix4.identity()..scale(0.96)) : Matrix4.identity(),
        decoration: BoxDecoration(
          color: _pressed ? AppColors.primary.withOpacity(0.08) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: _pressed ? AppColors.primary : AppColors.border),
          boxShadow: _pressed
              ? []
              : [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 6, offset: const Offset(0, 2))],
        ),
        child: Row(
          children: [
            Text(widget.icon, style: const TextStyle(fontSize: 18)),
            const SizedBox(width: 8),
            Text(widget.label, style: AppTextStyles.labelLarge),
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
