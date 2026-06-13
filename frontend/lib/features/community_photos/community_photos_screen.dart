import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/community_photos_provider.dart';
import '../../widgets/photo_grid.dart';
import '../../widgets/common/loading_widget.dart';
import '../../widgets/common/empty_state_widget.dart';

class CommunityPhotosScreen extends StatefulWidget {
  final String placeId;

  const CommunityPhotosScreen({super.key, required this.placeId});

  @override
  State<CommunityPhotosScreen> createState() => _CommunityPhotosScreenState();
}

class _CommunityPhotosScreenState extends State<CommunityPhotosScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CommunityPhotosProvider>().loadPhotos(widget.placeId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<CommunityPhotosProvider>();
    final photos = provider.photos;

    return Scaffold(
      appBar: AppBar(title: const Text('Community Photos')),
      body: photos.isEmpty
          ? EmptyStateWidget.noPhotos()
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: PhotoGrid(
                photoUrls: photos.map((p) => p.imageUrl).toList(),
                onTap: (index) {
                  // Open full screen viewer
                },
              ),
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Trigger image picker and upload
        },
        child: const Icon(Icons.add_a_photo_rounded),
      ),
    );
  }
}
