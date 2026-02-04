import 'package:flutter/material.dart';
import 'widgets/stock_tag.dart';
import 'widgets/depth_option.dart';

class AnalysisScreen extends StatefulWidget {
  const AnalysisScreen({super.key});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  final TextEditingController _searchController = TextEditingController();
  String _selectedDepth = 'Quick Analysis';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Container(
                padding: const EdgeInsets.all(16),
                color: const Color(0xFF2563EB),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        GestureDetector(
                          onTap: () {},
                          child: const Icon(Icons.arrow_back, color: Colors.white),
                        ),
                        const SizedBox(width: 16),
                        const Text(
                          'Stock Analysis',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Stock Code Input
                    const Text(
                      'Stock Code',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _searchController,
                      decoration: InputDecoration(
                        hintText: 'Enter stock code (e.g., HPG, VCB)',
                        hintStyle: TextStyle(color: Colors.grey[400], fontSize: 14),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: BorderSide(color: Colors.grey[300]!),
                        ),
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: BorderSide(color: Colors.grey[300]!),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: const BorderSide(color: Color(0xFF2563EB)),
                        ),
                        filled: true,
                        fillColor: Colors.grey[50],
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Popular Stocks
                    const Text(
                      'Popular Stocks',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        StockTag(code: 'VCB', onTap: () => _searchController.text = 'VCB'),
                        StockTag(code: 'HPG', onTap: () => _searchController.text = 'HPG'),
                        StockTag(code: 'VC', onTap: () => _searchController.text = 'VC'),
                        StockTag(code: 'FPT', onTap: () => _searchController.text = 'FPT'),
                        StockTag(code: 'VNM', onTap: () => _searchController.text = 'VNM'),
                        StockTag(code: 'GAS', onTap: () => _searchController.text = 'GAS'),
                        StockTag(code: 'TCB', onTap: () => _searchController.text = 'TCB'),
                        StockTag(code: 'MBB', onTap: () => _searchController.text = 'MBB'),
                      ],
                    ),
                    const SizedBox(height: 32),

                    // Analysis Depth
                    const Text(
                      'Analysis Depth',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Choose analysis scope (affects processing time)',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                    const SizedBox(height: 16),
                    DepthOption(
                      title: 'Quick Analysis',
                      subtitle: 'Basic overview - estimated 1 min',
                      isSelected: _selectedDepth == 'Quick Analysis',
                      onTap: () => setState(() => _selectedDepth = 'Quick Analysis'),
                    ),
                    const SizedBox(height: 12),
                    DepthOption(
                      title: 'Standard Analysis',
                      subtitle: 'Comprehensive analysis - 3-5 min',
                      isSelected: _selectedDepth == 'Standard Analysis',
                      onTap: () => setState(() => _selectedDepth = 'Standard Analysis'),
                    ),
                    const SizedBox(height: 12),
                    DepthOption(
                      title: 'Deep Analysis',
                      subtitle: 'In-depth investigation - 10-15 min',
                      isSelected: _selectedDepth == 'Deep Analysis',
                      onTap: () => setState(() => _selectedDepth = 'Deep Analysis'),
                    ),
                    const SizedBox(height: 32),

                    // Info Box
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: const Color(0xFF2563EB).withAlpha(25),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          const Icon(
                            Icons.info_outline,
                            color: Color(0xFF2563EB),
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              'Analysis typically takes +60 seconds to complete.',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey[700],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Start Analysis Button
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {},
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF2563EB),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        child: const Text(
                          'Start Analysis',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
