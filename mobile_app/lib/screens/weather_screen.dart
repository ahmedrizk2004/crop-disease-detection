import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/error_widget.dart';

class WeatherScreen extends StatefulWidget {
  const WeatherScreen({super.key});
  @override
  State<WeatherScreen> createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  bool _loading = false;
  Map<String, dynamic>? _data;
  String? _error;

  @override
  void initState() { super.initState(); _load(); }

  Future<void> _load() async {
    setState(() { _loading = true; _error = null; _data = null; });
    try {
      final res = await ApiService.getWeatherSummary();
      setState(() { _data = res; });
    } on ApiException catch (e) {
      setState(() { _error = e.message; });
    } catch (e) {
      setState(() { _error = '❌ خطأ غير متوقع: $e'; });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFFF3E0),
      appBar: AppBar(
        title: const Text('Weather Data', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFFE65100),
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [IconButton(icon: const Icon(Icons.refresh, color: Colors.white), onPressed: _load)],
      ),
      body: _loading
        ? const Center(child: CircularProgressIndicator(color: Color(0xFFE65100)))
        : _error != null
          ? Padding(
              padding: const EdgeInsets.all(20),
              child: AppErrorWidget(message: _error!, onRetry: _load))
          : _data == null
            ? const Center(child: Text('No data'))
            : _buildContent(),
    );
  }

  Widget _buildContent() {
    final d = _data!['data'] ?? {};
    return SingleChildScrollView(
      padding: const EdgeInsets.all(18),
      child: Column(children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(vertical: 24),
          decoration: BoxDecoration(
            gradient: const LinearGradient(colors: [Color(0xFFE65100), Color(0xFFFF8F00)],
              begin: Alignment.topLeft, end: Alignment.bottomRight),
            borderRadius: BorderRadius.circular(20),
          ),
          child: const Column(children: [
            Icon(Icons.wb_sunny, color: Colors.white, size: 48),
            SizedBox(height: 8),
            Text('Weather Summary', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
          ]),
        ),
        const SizedBox(height: 18),
        GridView.count(
          crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 12, mainAxisSpacing: 12, childAspectRatio: 1.1,
          children: [
            _StatCard('🌡️', 'Avg Temp',       '${d['avg_temperature'] ?? 0}°C', const Color(0xFFE53935)),
            _StatCard('💧', 'Avg Humidity',   '${d['avg_humidity'] ?? 0}%',     const Color(0xFF1565C0)),
            _StatCard('🌧️', 'Total Rainfall', '${d['total_rainfall'] ?? 0}mm',  const Color(0xFF00838F)),
            _StatCard('❄️', 'Frost Risk Days','${d['frost_risk_days'] ?? 0}',   const Color(0xFF6A1B9A)),
          ],
        ),
        if ((d['regions'] as List?)?.isNotEmpty == true) ...[
          const SizedBox(height: 18),
          Container(
            width: double.infinity, padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 8, offset: const Offset(0, 3))]),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('📍 Regions', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF1B5E20))),
              const SizedBox(height: 10),
              Wrap(spacing: 8, runSpacing: 8,
                children: (d['regions'] as List).map((r) => Chip(
                  label: Text('$r', style: const TextStyle(fontSize: 12)),
                  backgroundColor: const Color(0xFFFFF3E0),
                )).toList(),
              ),
            ]),
          ),
        ],
      ]),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String emoji, title, value;
  final Color color;
  const _StatCard(this.emoji, this.title, this.value, this.color);
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14),
        boxShadow: [BoxShadow(color: color.withOpacity(0.15), blurRadius: 8, offset: const Offset(0, 3))]),
      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(emoji, style: const TextStyle(fontSize: 26)),
        const SizedBox(height: 6),
        Text(value, style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color),
          textAlign: TextAlign.center, overflow: TextOverflow.ellipsis),
        const SizedBox(height: 4),
        Text(title, style: const TextStyle(fontSize: 11, color: Colors.grey),
          textAlign: TextAlign.center, maxLines: 2, overflow: TextOverflow.ellipsis),
      ]),
    );
  }
}
