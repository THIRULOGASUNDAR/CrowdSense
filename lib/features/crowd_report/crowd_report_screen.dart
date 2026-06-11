import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/crowd_provider.dart';
import '../../models/crowd_report_model.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/common/custom_button.dart';

class CrowdReportBottomSheet extends StatefulWidget {
  final String placeId;

  const CrowdReportBottomSheet({super.key, required this.placeId});

  @override
  State<CrowdReportBottomSheet> createState() => _CrowdReportBottomSheetState();
}

class _CrowdReportBottomSheetState extends State<CrowdReportBottomSheet> {
  CrowdReportLevel? _selectedLevel;
  final _noteController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Center(child: Container(width: 40, height: 4, decoration: BoxDecoration(color: Colors.grey.shade300, borderRadius: BorderRadius.circular(2)))),
          const SizedBox(height: 24),
          const Text('How crowded is it?', style: AppTextStyles.headlineMedium),
          const SizedBox(height: 8),
          const Text('Your live report helps others plan their travel.', style: AppTextStyles.bodyMedium),
          const SizedBox(height: 32),
          _buildOption(CrowdReportLevel.low, 'Not busy', 'Plenty of space, no queues.', AppColors.crowdLow),
          const SizedBox(height: 12),
          _buildOption(CrowdReportLevel.moderate, 'A bit busy', 'Moderate crowds, short wait.', AppColors.crowdModerate),
          const SizedBox(height: 12),
          _buildOption(CrowdReportLevel.high, 'Very crowded', 'Hard to move, long wait times.', AppColors.crowdHigh),
          const SizedBox(height: 24),
          TextField(
            controller: _noteController,
            decoration: const InputDecoration(
              hintText: 'Add an optional note...',
            ),
          ),
          const SizedBox(height: 32),
          CustomButton(
            text: 'Submit Report',
            onPressed: _selectedLevel == null ? null : _submit,
          ),
          SizedBox(height: MediaQuery.of(context).viewInsets.bottom),
        ],
      ),
    );
  }

  Widget _buildOption(CrowdReportLevel level, String title, String subtitle, Color color) {
    final isSelected = _selectedLevel == level;
    return GestureDetector(
      onTap: () => setState(() => _selectedLevel = level),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isSelected ? color.withOpacity(0.1) : Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: isSelected ? color : AppColors.border, width: 2),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: color.withOpacity(0.2), shape: BoxShape.circle),
              child: Icon(Icons.people_alt_rounded, color: color, size: 24),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: AppTextStyles.titleMedium.copyWith(color: isSelected ? color : null)),
                  Text(subtitle, style: AppTextStyles.bodySmall),
                ],
              ),
            ),
            if (isSelected) Icon(Icons.check_circle_rounded, color: color),
          ],
        ),
      ),
    );
  }

  void _submit() async {
    if (_selectedLevel != null) {
      await context.read<CrowdProvider>().submitReport(
        widget.placeId,
        _selectedLevel!,
        note: _noteController.text.trim(),
      );
      if (mounted) Navigator.pop(context);
    }
  }
}
