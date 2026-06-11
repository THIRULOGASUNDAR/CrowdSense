import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/place_provider.dart';
import '../../widgets/place_card.dart';
import 'package:go_router/go_router.dart';

class SearchResultsScreen extends StatelessWidget {
  const SearchResultsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final results = context.watch<PlaceProvider>().searchResults;

    return Scaffold(
      appBar: AppBar(title: const Text('Search Results')),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          childAspectRatio: 0.75,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
        ),
        itemCount: results.length,
        itemBuilder: (context, index) {
          final provider = context.read<PlaceProvider>();
          final place = provider.searchResults[index];
          return PlaceCard(
            place: place,
            onTap: () {
              provider.selectPlace(place);
              context.push('/place/${place.id}');
            },
          );
        },
      ),
    );
  }
}
