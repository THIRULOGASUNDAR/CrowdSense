import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../../providers/favorites_provider.dart';
import '../../providers/place_provider.dart';
import '../../widgets/place_card.dart';
import '../../widgets/common/empty_state_widget.dart';

class FavoritesScreen extends StatelessWidget {
  const FavoritesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final favorites = context.watch<FavoritesProvider>().favorites;

    return Scaffold(
      appBar: AppBar(title: const Text('Saved Places')),
      body: favorites.isEmpty
          ? EmptyStateWidget.noFavorites()
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: favorites.length,
              itemBuilder: (context, index) {
                final place = favorites[index];
                return Dismissible(
                  key: Key(place.id),
                  direction: DismissDirection.endToStart,
                  background: Container(
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20),
                    decoration: BoxDecoration(color: Colors.red, borderRadius: BorderRadius.circular(12)),
                    child: const Icon(Icons.delete_outline_rounded, color: Colors.white),
                  ),
                  onDismissed: (_) => context.read<FavoritesProvider>().toggleFavorite(place),
                  child: PlaceCard(
                    place: place,
                    onTap: () {
                      context.read<PlaceProvider>().selectPlace(place);
                      context.push('/place/${place.id}');
                    },
                  ),
                );
              },
            ),
    );
  }
}
