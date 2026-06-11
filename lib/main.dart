import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'firebase_options.dart';
import 'core/theme/app_theme.dart';
import 'providers/auth_provider.dart';
import 'providers/place_provider.dart';
import 'providers/crowd_provider.dart';
import 'providers/favorites_provider.dart';
import 'providers/community_photos_provider.dart';
import 'providers/travel_planner_provider.dart';
import 'providers/settings_provider.dart';
import 'providers/profile_provider.dart';
import 'services/fcm_service.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  // Initialize FCM (Optional, requires configuration in console)
  try {
    await FCMService().initialize();
  } catch (e) {
    debugPrint('FCM initialization skipped: $e');
  }
  
  runApp(const CrowdSenseApp());
}

class CrowdSenseApp extends StatelessWidget {
  const CrowdSenseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SettingsProvider()..load()),
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => PlaceProvider()),
        ChangeNotifierProvider(create: (_) => CrowdProvider()),
        ChangeNotifierProvider(create: (_) => FavoritesProvider()),
        ChangeNotifierProvider(create: (_) => CommunityPhotosProvider()),
        ChangeNotifierProvider(create: (_) => TravelPlannerProvider()),
        ChangeNotifierProvider(create: (_) => ProfileProvider()),
      ],
      child: Consumer<SettingsProvider>(
        builder: (context, settings, _) {
          return MaterialApp.router(
            title: 'CrowdSense',
            debugShowCheckedModeBanner: false,
            theme: AppTheme.lightTheme,
            darkTheme: AppTheme.darkTheme,
            themeMode: settings.themeMode,
            routerConfig: AppRouter.router,
          );
        },
      ),
    );
  }
}
