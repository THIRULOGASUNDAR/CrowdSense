import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../models/crowd_report_model.dart';
import '../../core/constants/app_config.dart';
import '../../core/constants/app_text_styles.dart';
import '../../core/utils/date_time_utils.dart';
import '../../widgets/common/loading_widget.dart';
import '../../widgets/common/empty_state_widget.dart';

class MyReportsScreen extends StatelessWidget {
  const MyReportsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;

    return Scaffold(
      appBar: AppBar(title: const Text('My Reports')),
      body: user == null
          ? const Center(child: Text('Please log in to view your reports.'))
          : StreamBuilder<List<CrowdReportModel>>(
              stream: FirebaseFirestore.instance
                  .collection(AppConfig.crowdReportsCollection)
                  .where('userId', isEqualTo: user.uid)
                  .orderBy('reportedAt', descending: true)
                  .snapshots()
                  .map((snapshot) => snapshot.docs
                      .map((doc) => CrowdReportModel.fromFirestore(doc))
                      .toList()),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return Center(child: Text('Error: ${snapshot.error}'));
                }
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CrowdSenseLoading();
                }

                final reports = snapshot.data ?? [];

                if (reports.isEmpty) {
                  return const EmptyStateWidget(
                    icon: Icons.history_rounded,
                    title: 'No reports yet',
                    subtitle: 'Your crowd reports will appear here.',
                  );
                }

                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: reports.length,
                  itemBuilder: (context, index) {
                    final report = reports[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        title: Text(report.level.name.toUpperCase(), 
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: _getColor(report.level),
                          ),
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            if (report.note != null && report.note!.isNotEmpty)
                              Text('"${report.note}"', style: AppTextStyles.bodyMedium),
                            const SizedBox(height: 4),
                            Text(DateTimeUtils.formatDateTime(report.reportedAt), style: AppTextStyles.caption),
                          ],
                        ),
                        trailing: const Icon(Icons.chevron_right_rounded),
                        onTap: () {
                          // Navigate to place details if possible
                        },
                      ),
                    );
                  },
                );
              },
            ),
    );
  }

  Color _getColor(CrowdReportLevel level) {
    switch (level) {
      case CrowdReportLevel.low: return Colors.green;
      case CrowdReportLevel.moderate: return Colors.orange;
      case CrowdReportLevel.high: return Colors.red;
    }
  }
}
