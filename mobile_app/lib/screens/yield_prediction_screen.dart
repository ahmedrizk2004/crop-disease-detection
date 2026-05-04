import 'package:flutter/material.dart';
import '../services/api_service.dart';

class YieldPredictionScreen extends StatefulWidget {
  const YieldPredictionScreen({super.key});
  @override
  State<YieldPredictionScreen> createState() => _YieldPredictionScreenState();
}

class _YieldPredictionScreenState extends State<YieldPredictionScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _loading = false;
  Map<String, dynamic>? _result;

  String _cropType = 'Wheat';
  String _soilType = 'Loamy';
  String _season   = 'Summer';

  final _temp       = TextEditingController(text: '25');
  final _humidity   = TextEditingController(text: '65');
  final _rainfall   = TextEditingController(text: '20');
  final _nitrogen   = TextEditingController(text: '60');
  final _phosphorus = TextEditingController(text: '35');
  final _potassium  = TextEditingController(text: '90');
  final _severity   = TextEditingController(text: '0.1');

  final List<String> _crops   = ['Wheat','Rice','Corn','Tomato','Potato'];
  final List<String> _soils   = ['Loamy','Sandy','Clay','Silty','Peaty'];
  final List<String> _seasons = ['Summer','Winter','Spring','Autumn'];

  Future<void> _predict() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() { _loading = true; _result = null; });
    try {
      final n = double.parse(_nitrogen.text);
      final p = double.parse(_phosphorus.text);
      final k = double.parse(_potassium.text);
      final data = {
        'crop_type': _cropType, 'soil_type': _soilType, 'season': _season,
        'temperature_c': double.parse(_temp.text),
        'humidity_pct':  double.parse(_humidity.text),
        'rainfall_mm':   double.parse(_rainfall.text),
        'nitrogen_ppm':  n, 'phosphorus_ppm': p, 'potassium_ppm': k,
        'disease_severity': double.parse(_severity.text),
        'npk_total': n + p + k, 'is_diseased': double.parse(_severity.text) > 0.3 ? 1 : 0,
      };
      final res = await ApiService.predictYield(data);
      setState(() { _result = res; });
    } catch (e) {
      setState(() { _result = {'error': e.toString()}; });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF1F8E9),
      appBar: AppBar(
        title: const Text('Yield Prediction', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1565C0),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Form(
          key: _formKey,
          child: Column(children: [
            _buildCard('🌾 Crop Info', [
              _buildDropdown('Crop Type', _crops, _cropType, (v) => setState(() => _cropType = v!)),
              _buildDropdown('Soil Type', _soils, _soilType, (v) => setState(() => _soilType = v!)),
              _buildDropdown('Season',    _seasons, _season,  (v) => setState(() => _season   = v!)),
            ]),
            const SizedBox(height: 14),
            _buildCard('🌡️ Conditions', [
              _buildField(_temp,     'Temperature (°C)', '0-55'),
              _buildField(_humidity, 'Humidity (%)',     '0-100'),
              _buildField(_rainfall, 'Rainfall (mm)',    '≥ 0'),
            ]),
            const SizedBox(height: 14),
            _buildCard('🧪 Nutrients (ppm)', [
              _buildField(_nitrogen,   'Nitrogen',   '≥ 0'),
              _buildField(_phosphorus, 'Phosphorus', '≥ 0'),
              _buildField(_potassium,  'Potassium',  '≥ 0'),
              _buildField(_severity,   'Disease Severity (0-1)', '0.0-1.0'),
            ]),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity, height: 50,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _predict,
                icon: _loading ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white)) : const Icon(Icons.trending_up, color: Colors.white),
                label: Text(_loading ? 'Predicting...' : 'Predict Yield', style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1565C0), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
              ),
            ),
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
        const SizedBox(height: 12), ...fields,
      ]),
    );
  }

  Widget _buildDropdown(String label, List<String> items, String value, ValueChanged<String?> onChanged) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: DropdownButtonFormField<String>(
        value: value, onChanged: onChanged, items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
        decoration: InputDecoration(labelText: label, border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
      ),
    );
  }

  Widget _buildField(TextEditingController c, String label, String hint) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: TextFormField(
        controller: c, keyboardType: const TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(labelText: label, hintText: hint,
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
        validator: (v) => (v == null || v.isEmpty) ? 'Required' : null,
      ),
    );
  }

  Widget _buildResult() {
    if (_result!.containsKey('error')) {
      return Container(padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: const Color(0xFFFFEBEE), borderRadius: BorderRadius.circular(14)),
        child: Text('❌ ${_result!['error']}', style: const TextStyle(color: Color(0xFFB71C1C))));
    }
    final yield_ = _result!['data']?['predicted_yield_kg_per_hectare'] ?? 0;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Color(0xFF1565C0), Color(0xFF42A5F5)], begin: Alignment.topLeft, end: Alignment.bottomRight),
        borderRadius: BorderRadius.circular(16)),
      child: Column(children: [
        const Text('🌾 Predicted Yield', style: TextStyle(color: Colors.white70, fontSize: 14)),
        const SizedBox(height: 8),
        Text('$yield_', style: const TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
        const Text('kg / hectare', style: TextStyle(color: Colors.white70, fontSize: 13)),
      ]),
    );
  }
}
