import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class PhotoGrid extends StatelessWidget {
  final List<String> photoUrls;
  final Function(int)? onTap;

  const PhotoGrid({
    super.key,
    required this.photoUrls,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
      ),
      itemCount: photoUrls.length,
      itemBuilder: (context, index) {
        return GestureDetector(
          onTap: () => onTap?.call(index),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: CachedNetworkImage(
              imageUrl: photoUrls[index],
              fit: BoxFit.cover,
              placeholder: (context, url) => Container(color: Colors.grey.shade200),
              errorWidget: (context, url, error) => const Icon(Icons.error),
            ),
          ),
        );
      },
    );
  }
}
