import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/error_widget.dart';

class DiseaseDetectionScreen extends StatefulWidget {
  const DiseaseDetectionScreen({super.key});
  @override
  State<DiseaseDetectionScreen> createState() => _DiseaseDetectionScreenState();
}

class _DiseaseDetectionScreenState extends State<DiseaseDetectionScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _loading = false;
  Map<String, dynamic>? _result;
  String? _error;

  final _temp       = TextEditingController(text: '28');
  final _humidity   = TextEditingController(text: '70');
  final _rainfall   = TextEditingController(text: '15');
  final _nitrogen   = TextEditingController(text: '50');
  final _phosphorus = TextEditingController(text: '30');
  final _potassium  = TextEditingController(text: '80');
  final _severity   = TextEditingController(text: '0.3');

  Future<void> _predict() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() { _loading = true; _result = null; _error = null; });
    try {
      final npk = double.parse(_nitrogen.text) + double.parse(_phosphorus.text) + double.parse(_potassium.text);
      final res = await ApiService.predictDisease({
        'temperature_c':    double.parse(_temp.text),
        'humidity_pct':     double.parse(_humidity.text),
        'rainfall_mm':      double.parse(_rainfall.text),
        'nitrogen_ppm':     double.parse(_nitrogen.text),
        'phosphorus_ppm':   double.parse(_phosphorus.text),
        'potassium_ppm':    double.parse(_potassium.text),
        'disease_severity': double.parse(_severity.text),
        'npk_total':        npk,
      });
      setState(() { _result = res; });
    } on ApiException catch (e) {
      setState(() { _error = e.message; });
    } catch (e) {
      setState(() { _error = 'Error: $e'; });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F8E9),
      appBar: AppBar(
        title: const Text('Disease Detection', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFFE53935),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Form(
          key: _formKey,
          child: Column(children: [
            _buildCard('Environmental Data', [
              _buildField(_temp,      'Temperature (C)',  '0-55'),
              _buildField(_humidity,  'Humidity (%)',     '0-100'),
              _buildField(_rainfall,  'Rainfall (mm)',    '>= 0'),
            ]),
            const SizedBox(height: 14),
            _buildCard('Soil Nutrients (ppm)', [
              _buildField(_nitrogen,   'Nitrogen',   '>= 0'),
              _buildField(_phosphorus, 'Phosphorus', '>= 0'),
              _buildField(_potassium,  'Potassium',  '>= 0'),
            ]),
            const SizedBox(height: 14),
            _buildCard('Disease Severity', [
              _buildField(_severity, 'Severity (0.0 - 1.0)', '0.0-1.0'),
            ]),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity, height: 50,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _predict,
                icon: _loading
                  ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.search, color: Colors.white),
                label: Text(_loading ? 'Analyzing...' : 'Detect Disease',
                  style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFE53935),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 16),
              AppErrorWidget(message: _error!, onRetry: _predict),
            ],
            if (_result != null) ...[const SizedBox(height: 20), _buildResult()],
          ]),
        ),
      ),
    );
  }

  Widget _buildCard(String title, List<Widget> fields) {
    return Container(
      width: double.infinity, padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 8, offset: const Offset(0, 3))]),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF1B5E20))),
        const SizedBox(height: 12),
        ...fields,
      ]),
    );
  }

  Widget _buildField(TextEditingController c, String label, String hint) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: TextFormField(
        controller: c,
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(labelText: label, hintText: hint,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
        validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
      ),
    );
  }

  Widget _buildResult() {
    final data      = _result!['data'] ?? {};
    final disease   = data['disease']    ?? 'Unknown';
    final confidence= data['confidence'] ?? 0;
    final isHealthy = disease == 'Healthy';
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: isHealthy ? const Color(0xFFE8F5E9) : const Color(0xFFFFEBEE),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: isHealthy ? const Color(0xFF2E7D32) : const Color(0xFFE53935), width: 1.5),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(isHealthy ? 'Plant is Healthy!' : 'Disease Detected!',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16,
            color: isHealthy ? const Color(0xFF2E7D32) : const Color(0xFFE53935))),
        const SizedBox(height: 10),
        _row('Disease',    disease),
        _row('Confidence', '$confidence%'),
      ]),
    );
  }

  Widget _row(String label, String value) => Padding(
    padding: const EdgeInsets.symmetric(vertical: 4),
    child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
      Text(label, style: const TextStyle(color: Colors.grey)),
      Text(value,  style: const TextStyle(fontWeight: FontWeight.bold)),
    ]),
  );
}
