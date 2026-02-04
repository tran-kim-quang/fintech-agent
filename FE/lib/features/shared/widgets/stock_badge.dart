import 'package:flutter/material.dart';

class StockBadge extends StatelessWidget {
  final String label;
  final Color color;

  const StockBadge({
    super.key,
    required this.label,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withAlpha(50),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color.withAlpha(255),
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
