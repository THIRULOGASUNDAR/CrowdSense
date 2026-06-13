import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../providers/auth_provider.dart';
import '../../providers/profile_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../core/constants/app_text_styles.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage(ProfileProvider provider) async {
    final XFile? image = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 70,
      maxWidth: 512,
    );

    if (image != null) {
      await provider.updateProfilePhoto(File(image.path));
    }
  }

  void _showEditProfileDialog(BuildContext context, ProfileProvider provider) {
    final nameController = TextEditingController(text: provider.userProfile?.displayName);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Edit Profile'),
        content: CustomTextField(
          label: 'Display Name',
          hint: 'Enter your name',
          controller: nameController,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              provider.updateDisplayName(nameController.text.trim());
              Navigator.pop(context);
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final authProvider = context.watch<AuthProvider>();
    final profileProvider = context.watch<ProfileProvider>();
    
    final user = authProvider.currentUser;
    final profile = profileProvider.userProfile;
    final isLoading = profileProvider.isLoading;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
        actions: [
          IconButton(icon: const Icon(Icons.settings_outlined), onPressed: () => context.push('/settings')),
        ],
      ),
      body: Stack(
        children: [
          SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Center(
                  child: GestureDetector(
                    onTap: () => _pickImage(profileProvider),
                    child: Stack(
                      children: [
                        CircleAvatar(
                          radius: 60,
                          backgroundColor: AppColors.surfaceVariant,
                          backgroundImage: profile?.photoUrl != null 
                              ? NetworkImage(profile!.photoUrl!) 
                              : (user?.photoURL != null ? NetworkImage(user!.photoURL!) : null),
                          child: (profile?.photoUrl == null && user?.photoURL == null) 
                              ? const Icon(Icons.person, size: 60, color: AppColors.textHint) 
                              : null,
                        ),
                        Positioned(
                          bottom: 0,
                          right: 0,
                          child: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                            child: const Icon(Icons.camera_alt_rounded, color: Colors.white, size: 20),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),
                Text(
                  profile?.displayName ?? user?.displayName ?? 'Anonymous User', 
                  style: AppTextStyles.headlineLarge,
                  textAlign: TextAlign.center,
                ),
                Text(user?.email ?? '', style: AppTextStyles.bodyMedium),
                const SizedBox(height: 32),
                Row(
                  children: [
                    Expanded(child: _buildStat('Photos', profile?.uploadedPhotos.length.toString() ?? '0')),
                    Expanded(child: _buildStat('Reports', profile?.totalReports.toString() ?? '0')),
                    Expanded(child: _buildStat('Saved', profile?.savedPlaces.length.toString() ?? '0')),
                  ],
                ),
                const SizedBox(height: 48),
                _buildMenuItem(Icons.person_outline_rounded, 'Edit Profile', () => _showEditProfileDialog(context, profileProvider)),
                _buildMenuItem(Icons.notifications_none_rounded, 'Notifications', () => context.push('/settings')),
                _buildMenuItem(Icons.history_rounded, 'My Reports', () => context.push('/my-reports')),
                _buildMenuItem(Icons.help_outline_rounded, 'Support & FAQ', () async {
                  final Uri url = Uri.parse('mailto:support@crowdsense.app');
                  if (await canLaunchUrl(url)) {
                    await launchUrl(url);
                  }
                }),
                const SizedBox(height: 32),
                CustomButton(
                  text: 'Sign Out',
                  variant: ButtonVariant.outline,
                  onPressed: () => authProvider.signOut(),
                ),
              ],
            ),
          ),
          if (isLoading)
            Container(
              color: Colors.black26,
              child: const Center(child: CircularProgressIndicator()),
            ),
        ],
      ),
    );
  }

  Widget _buildStat(String label, String value) {
    return Column(
      children: [
        Text(value, style: AppTextStyles.headlineMedium.copyWith(color: AppColors.primary)),
        Text(label, style: AppTextStyles.bodySmall),
      ],
    );
  }

  Widget _buildMenuItem(IconData icon, String title, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppColors.textPrimary),
      title: Text(title, style: AppTextStyles.titleMedium),
      trailing: const Icon(Icons.chevron_right_rounded),
      onTap: onTap,
    );
  }
}
