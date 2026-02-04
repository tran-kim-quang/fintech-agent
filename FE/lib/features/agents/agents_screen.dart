import 'package:flutter/material.dart';
import 'widgets/agent_item.dart';
import '../shared/widgets/screen_header.dart';

class AgentsScreen extends StatefulWidget {
  const AgentsScreen({super.key});

  @override
  State<AgentsScreen> createState() => _AgentsScreenState();
}

class _AgentsScreenState extends State<AgentsScreen> {
  double _progressValue = 0.6;

  @override
  void initState() {
    super.initState();
    _startProgressAnimation();
  }

  void _startProgressAnimation() {
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted && _progressValue < 1.0) {
        setState(() {
          _progressValue += 0.1;
        });
        _startProgressAnimation();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Agents Processing'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            ScreenHeader(
              title: 'Analyzing HPG',
              trailing: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withAlpha(230),
                  borderRadius: BorderRadius.circular(8),
                ),
                padding: const EdgeInsets.all(8),
                child: const Icon(
                  Icons.close,
                  color: Color(0xFF2563EB),
                  size: 20,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Analysis Progress
                  const Text(
                    'Analysis Progress',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Complete',
                        style: TextStyle(fontSize: 12),
                      ),
                      Text(
                        '${(_progressValue * 100).toStringAsFixed(0)}%',
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF2563EB),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: _progressValue,
                      minHeight: 8,
                      backgroundColor: Colors.grey[300],
                      valueColor: const AlwaysStoppedAnimation<Color>(Color(0xFF2563EB)),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // AI Agents Section
                  const Text(
                    'AI Agents',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const AgentItem(
                    title: 'Fundamental Agent',
                    description: 'Analyzing fundamental indicators, balance sheet, cash flow',
                    icon: Icons.bar_chart,
                    isCompleted: true,
                  ),
                  const SizedBox(height: 12),
                  const AgentItem(
                    title: 'Technical Agent',
                    description: 'Analyzing technical patterns and support/resistance levels',
                    icon: Icons.trending_up,
                    isCompleted: true,
                  ),
                  const SizedBox(height: 12),
                  const AgentItem(
                    title: 'News Sentiment Agent',
                    description: 'Processing related news and market sentiment analysis',
                    icon: Icons.newspaper,
                    isCompleted: false,
                  ),
                  const SizedBox(height: 12),
                  const AgentItem(
                    title: 'Risk Management Agent',
                    description: 'Risk factors assessment & recommendations',
                    icon: Icons.security,
                    isCompleted: false,
                  ),
                  const SizedBox(height: 24),

                  // Info Box
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue[50],
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.blue[200]!),
                    ),
                    child: const Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Multi-pronged processing are visible in the final report, ensuring you understand their context.',
                          style: TextStyle(
                            fontSize: 12,
                            color: Color(0xFF2563EB),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Cancel Button
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: () {},
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 12),
                        side: const BorderSide(color: Colors.grey),
                      ),
                      child: const Text('Cancel Analysis'),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
