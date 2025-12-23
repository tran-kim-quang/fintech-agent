import 'package:flutter/material.dart';

class ScreenHeader extends StatelessWidget {
  final String title;
  final IconData? icon;
  final bool showBackButton;
  final VoidCallback? onBackPressed;
  final Widget? trailing;

  const ScreenHeader({
    super.key,
    required this.title,
    this.icon,
    this.showBackButton = false,
    this.onBackPressed,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFF2563EB),
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          if (showBackButton)
            GestureDetector(
              onTap: onBackPressed ?? () => Navigator.of(context).pop(),
              child: const Icon(Icons.arrow_back, color: Colors.white),
            ),
          if (showBackButton) const SizedBox(width: 12),
          if (icon != null)
            Container(
              decoration: BoxDecoration(
                color: Colors.white.withAlpha(230),
                borderRadius: BorderRadius.circular(8),
              ),
              padding: const EdgeInsets.all(8),
              child: Icon(
                icon,
                color: const Color(0xFF2563EB),
                size: 24,
              ),
            ),
          if (icon != null) const SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          if (trailing != null) trailing!,
        ],
      ),
    );
  }
}
