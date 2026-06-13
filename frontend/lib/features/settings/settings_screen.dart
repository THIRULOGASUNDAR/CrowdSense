import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/settings_provider.dart';
import '../../core/constants/app_text_styles.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = context.watch<SettingsProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          _buildHeader('Appearance'),
          SwitchListTile(
            title: const Text('Dark Mode'),
            subtitle: const Text('Reduce eye strain in low light'),
            value: settings.themeMode == ThemeMode.dark,
            onChanged: (value) => settings.toggleTheme(),
          ),
          _buildHeader('Notifications'),
          SwitchListTile(
            title: const Text('Push Notifications'),
            subtitle: const Text('Get alerts for crowd levels and trip plans'),
            value: settings.notificationsEnabled,
            onChanged: (value) => settings.setNotifications(value),
          ),
          _buildHeader('About'),
          ListTile(
            title: const Text('Privacy Policy'),
            trailing: const Icon(Icons.open_in_new_rounded, size: 20),
            onTap: () {},
          ),
          ListTile(
            title: const Text('Terms of Service'),
            trailing: const Icon(Icons.open_in_new_rounded, size: 20),
            onTap: () {},
          ),
          const ListTile(
            title: Text('App Version'),
            trailing: Text('1.0.0 (Build 1)'),
          ),
          _buildHeader('Account'),
          ListTile(
            title: const Text('Delete Account', style: TextStyle(color: Colors.red)),
            onTap: () {},
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
      child: Text(
        title.toUpperCase(),
        style: AppTextStyles.labelLarge.copyWith(color: Colors.grey, fontSize: 12),
      ),
    );
  }
}
