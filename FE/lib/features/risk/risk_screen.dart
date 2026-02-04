import 'package:flutter/material.dart';
import 'widgets/allocation_card.dart';
import 'widgets/position_item.dart';
import '../shared/widgets/screen_header.dart';

class RiskScreen extends StatefulWidget {
  const RiskScreen({super.key});

  @override
  State<RiskScreen> createState() => _RiskScreenState();
}

class _RiskScreenState extends State<RiskScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Risk Management'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            const ScreenHeader(
              title: 'Risk Management',
              icon: Icons.security,
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Overall Portfolio Risk
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Overall Portfolio Risk',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: Colors.orange[100],
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Row(
                          children: [
                            Icon(Icons.warning, color: Colors.orange[700], size: 16),
                            const SizedBox(width: 4),
                            Text(
                              'High',
                              style: TextStyle(
                                color: Colors.orange[700],
                                fontWeight: FontWeight.bold,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    '5.2',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Medium Risk Portfolio
                  _buildRiskCard(
                    'Medium Risk - Portfolio is well-diversified.',
                    'Expected volatility: 18.5%',
                    'Potential drawdown: 12.3%',
                  ),
                  const SizedBox(height: 24),

                  // Portfolio Allocation
                  const Text(
                    'Portfolio Allocation',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Row(
                    children: [
                      Expanded(
                        child: AllocationCard(
                          title: 'STOCKS',
                          percentage: '45%',
                          description: 'Diversified across sectors',
                        ),
                      ),
                      SizedBox(width: 8),
                      Expanded(
                        child: AllocationCard(
                          title: 'BONDS',
                          percentage: '35%',
                          description: 'Government and Corporate',
                        ),
                      ),
                      SizedBox(width: 8),
                      Expanded(
                        child: AllocationCard(
                          title: 'CASH',
                          percentage: '20%',
                          description: 'Emergency reserve',
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // Pie Chart Placeholder
                  const Text(
                    'Asset Allocation Breakdown',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  _buildPieChartPlaceholder(),
                  const SizedBox(height: 24),

                  // Individual Positions
                  const Text(
                    'Individual Positions',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const PositionItem(code: 'VCB', name: 'Vietcombank', percentage: '25%', color: Colors.blue),
                  const SizedBox(height: 8),
                  const PositionItem(code: 'HPG', name: 'Hoa Phat', percentage: '20%', color: Colors.green),
                  const SizedBox(height: 8),
                  const PositionItem(code: 'TCB', name: 'Techcombank', percentage: '15%', color: Colors.red),
                  const SizedBox(height: 8),
                  const PositionItem(code: 'FPT', name: 'FPT Software', percentage: '10%', color: Colors.orange),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRiskCard(String title, String subtitle1, String subtitle2) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 13,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            subtitle1,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            subtitle2,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPieChartPlaceholder() {
    return Container(
      height: 250,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey[300]!),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 150,
              height: 150,
              decoration: const BoxDecoration(
                shape: BoxShape.circle,
                gradient: LinearGradient(
                  colors: [
                    Colors.blue,
                    Colors.green,
                    Colors.orange,
                    Colors.purple,
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'Asset Allocation Pie Chart',
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
