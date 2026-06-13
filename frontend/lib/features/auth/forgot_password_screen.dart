import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../core/constants/app_text_styles.dart';
import '../../core/constants/app_colors.dart';
import '../../core/utils/validators.dart';

class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  bool _isSubmitted = false;

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  void _onReset() async {
    if (_formKey.currentState!.validate()) {
      await context.read<AuthProvider>().sendPasswordReset(_emailController.text.trim());
      
      if (!mounted) return;
      
      final error = context.read<AuthProvider>().errorMessage;
      if (error != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error), backgroundColor: AppColors.error),
        );
      } else {
        setState(() => _isSubmitted = true);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isLoading = context.watch<AuthProvider>().isLoading;

    return Scaffold(
      appBar: AppBar(backgroundColor: Colors.transparent, elevation: 0),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: _isSubmitted
              ? Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.mark_email_read_outlined, size: 80, color: AppColors.success),
                    const SizedBox(height: 24),
                    const Text('Check Your Email', style: AppTextStyles.headlineLarge),
                    const SizedBox(height: 12),
                    const Text(
                      'We have sent a password reset link to your email address.',
                      textAlign: TextAlign.center,
                      style: AppTextStyles.bodyMedium,
                    ),
                    const SizedBox(height: 40),
                    CustomButton(
                      text: 'Back to Login',
                      onPressed: () => Navigator.of(context).pop(),
                    ),
                  ],
                )
              : Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Reset Password', style: AppTextStyles.displayLarge),
                      const SizedBox(height: 8),
                      const Text(
                        'Enter your email and we\'ll send you instructions to reset your password.',
                        style: AppTextStyles.bodyMedium,
                      ),
                      const SizedBox(height: 48),
                      CustomTextField(
                        label: 'Email Address',
                        hint: 'Enter your email',
                        controller: _emailController,
                        keyboardType: TextInputType.emailAddress,
                        prefixIcon: Icons.email_outlined,
                        validator: Validators.validateEmail,
                      ),
                      const SizedBox(height: 32),
                      CustomButton(
                        text: 'Send Reset Link',
                        onPressed: _onReset,
                        isLoading: isLoading,
                      ),
                    ],
                  ),
                ),
        ),
      ),
    );
  }
}
