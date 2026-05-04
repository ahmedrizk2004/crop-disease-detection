import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../services/api_service.dart';

class PlantAnalyzerScreen extends StatefulWidget {
  const PlantAnalyzerScreen({super.key});
  @override
  State<PlantAnalyzerScreen> createState() => _PlantAnalyzerScreenState();
}

class _PlantAnalyzerScreenState extends State<PlantAnalyzerScreen> {
  File? _image;
  bool _loading = false;
  Map<String, dynamic>? _analysis;
  final _picker = ImagePicker();
  String _cropType = 'Tomato';
  final _symptomsCtrl = TextEditingController(text: 'yellow leaves, brown spots');
  final List<String> _crops = ['Wheat', 'Rice', 'Corn', 'Tomato', 'Potato'];

  Future<void> _pickImage(ImageSource source) async {
    final picked = await _picker.pickImage(source: source, imageQuality: 80);
    if (picked != null) setState(() { _image = File(picked.path); _analysis = null; });
  }

  Future<void> _analyzeImage() async {
    if (_image == null) return;
    setState(() { _loading = true; _analysis = null; });
    try {
      final res = await ApiService.analyzePlantImage(_image!);
      if (res['success'] == true) {
        setState(() { _analysis = res['analysis'] as Map<String, dynamic>; });
      } else {
        setState(() { _analysis = {'error': res['error'] ?? 'Unknown error'}; });
      }
    } catch (e) {
      setState(() { _analysis = {'error': e.toString()}; });
    } finally {
      setState(() { _loading = false; });
    }
  }

  Future<void> _analyzeData() async {
    setState(() { _loading = true; _analysis = null; });
    try {
      final symptoms = _symptomsCtrl.text.split(',').map((e) => e.trim()).toList();
      final res = await ApiService.analyzePlantData(_cropType, symptoms, {
        'temperature_c': 30, 'humidity_pct': 75, 'rainfall_mm': 10,
        'soil_type': 'Loamy', 'nitrogen_ppm': 45, 'phosphorus_ppm': 25, 'potassium_ppm': 85,
      });
      if (res['success'] == true) {
        setState(() { _analysis = res['analysis'] as Map<String, dynamic>; });
      } else {
        setState(() { _analysis = {'error': res['error'] ?? 'Unknown error'}; });
      }
    } catch (e) {
      setState(() { _analysis = {'error': e.toString()}; });
    } finally {
      setState(() { _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF3E5F5),
      appBar: AppBar(
        title: const Text('AI Plant Analyzer', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF6A1B9A),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(18),
        child: Column(children: [
          // ── Image Section ──
          Container(
            width: double.infinity, padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 8, offset: const Offset(0, 3))]),
            child: Column(children: [
              const Text('📸 Analyze by Image',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF4A148C))),
              const SizedBox(height: 12),
              GestureDetector(
                onTap: () => _pickImage(ImageSource.gallery),
                child: Container(
                  height: 160, width: double.infinity,
                  decoration: BoxDecoration(
                    color: const Color(0xFFEDE7F6), borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF9C27B0))),
                  child: _image != null
                    ? ClipRRect(borderRadius: BorderRadius.circular(12), child: Image.file(_image!, fit: BoxFit.cover))
                    : const Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Icon(Icons.add_photo_alternate, size: 48, color: Color(0xFF9C27B0)),
                        SizedBox(height: 8),
                        Text('Tap to select image', style: TextStyle(color: Color(0xFF9C27B0))),
                      ]),
                ),
              ),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(child: OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library, size: 18),
                  label: const Text('Gallery'),
                  style: OutlinedButton.styleFrom(foregroundColor: const Color(0xFF6A1B9A)),
                )),
                const SizedBox(width: 10),
                Expanded(child: OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.camera),
                  icon: const Icon(Icons.camera_alt, size: 18),
                  label: const Text('Camera'),
                  style: OutlinedButton.styleFrom(foregroundColor: const Color(0xFF6A1B9A)),
                )),
              ]),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity, height: 46,
                child: ElevatedButton.icon(
                  onPressed: (_loading || _image == null) ? null : _analyzeImage,
                  icon: const Icon(Icons.document_scanner, color: Colors.white, size: 18),
                  label: const Text('Analyze Image', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF6A1B9A),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10))),
                ),
              ),
            ]),
          ),
          const SizedBox(height: 14),
          // ── Symptoms Section ──
          Container(
            width: double.infinity, padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 8, offset: const Offset(0, 3))]),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('📋 Analyze by Symptoms',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF4A148C))),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: _cropType, onChanged: (v) => setState(() => _cropType = v!),
                items: _crops.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                decoration: InputDecoration(labelText: 'Crop Type',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
              ),
              const SizedBox(height: 10),
              TextFormField(
                controller: _symptomsCtrl, maxLines: 2,
                decoration: InputDecoration(
                  labelText: 'Symptoms (comma separated)',
                  hintText: 'e.g. yellow leaves, brown spots',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10)),
              ),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity, height: 46,
                child: ElevatedButton.icon(
                  onPressed: _loading ? null : _analyzeData,
                  icon: _loading
                    ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.psychology, color: Colors.white, size: 18),
                  label: Text(_loading ? 'Analyzing...' : 'Analyze Symptoms',
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF6A1B9A),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10))),
                ),
              ),
            ]),
          ),
          // ── Result ──
          if (_analysis != null) ...[const SizedBox(height: 16), _buildResult()],
        ]),
      ),
    );
  }

  Widget _buildResult() {
    if (_analysis!.containsKey('error')) {
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: const Color(0xFFFFEBEE), borderRadius: BorderRadius.circular(14)),
        child: Text('❌ ${_analysis!['error']}', style: const TextStyle(color: Color(0xFFB71C1C))),
      );
    }

    final disease  = _analysis!['disease_name']  ?? 'Unknown';
    final severity = _analysis!['severity']       ?? 'Unknown';
    final sevScore = ((_analysis!['severity_score'] ?? 0) * 100).toStringAsFixed(0);
    final conf     = ((_analysis!['confidence']     ?? 0) * 100).toStringAsFixed(0);
    final urgency  = _analysis!['urgency']           ?? 'Unknown';
    final yieldLoss= _analysis!['estimated_yield_loss'] ?? 0;
    final symptoms = (_analysis!['symptoms'] as List?)  ?? [];
    final immediate= (_analysis!['treatment']?['immediate'] as List?) ?? [];
    final longterm = (_analysis!['treatment']?['longterm']  as List?) ?? [];
    final prevention=(_analysis!['prevention'] as List?)   ?? [];
    final rec      = _analysis!['recommendation'] ?? '';

    Color urgencyColor = urgency == 'Critical' ? Colors.red
      : urgency == 'High' ? Colors.orange
      : urgency == 'Medium' ? Colors.amber
      : Colors.green;

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFF6A1B9A), width: 1.5),
        boxShadow: [BoxShadow(color: Colors.purple.withOpacity(0.1), blurRadius: 10, offset: const Offset(0, 4))]),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        const Text('🤖 AI Analysis Result',
          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF4A148C))),
        const Divider(height: 20),

        // Disease name banner
        Container(
          width: double.infinity, padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: const Color(0xFFEDE7F6), borderRadius: BorderRadius.circular(10)),
          child: Text('🦠 $disease',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF4A148C))),
        ),
        const SizedBox(height: 12),

        _row('⚠️ Severity',    '$severity ($sevScore%)'),
        _row('🎯 Confidence',  '$conf%'),
        _row('📉 Yield Loss',  '$yieldLoss%'),
        // Urgency badge
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            const Text('🚨 Urgency', style: TextStyle(color: Colors.grey, fontSize: 13)),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
              decoration: BoxDecoration(color: urgencyColor.withOpacity(0.15), borderRadius: BorderRadius.circular(20)),
              child: Text(urgency, style: TextStyle(color: urgencyColor, fontWeight: FontWeight.bold, fontSize: 13)),
            ),
          ]),
        ),

        if (symptoms.isNotEmpty) ...[
          const SizedBox(height: 12),
          const Text('📋 Symptoms:', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF4A148C))),
          const SizedBox(height: 4),
          ...symptoms.map((s) => Padding(padding: const EdgeInsets.only(left: 8, bottom: 2),
            child: Text('• $s', style: const TextStyle(fontSize: 13)))),
        ],

        if (immediate.isNotEmpty) ...[
          const SizedBox(height: 12),
          const Text('💊 Immediate Treatment:', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF4A148C))),
          const SizedBox(height: 4),
          ...immediate.map((s) => Padding(padding: const EdgeInsets.only(left: 8, bottom: 2),
            child: Text('• $s', style: const TextStyle(fontSize: 13)))),
        ],

        if (longterm.isNotEmpty) ...[
          const SizedBox(height: 12),
          const Text('🔬 Long-term Treatment:', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF4A148C))),
          const SizedBox(height: 4),
          ...longterm.map((s) => Padding(padding: const EdgeInsets.only(left: 8, bottom: 2),
            child: Text('• $s', style: const TextStyle(fontSize: 13)))),
        ],

        if (prevention.isNotEmpty) ...[
          const SizedBox(height: 12),
          const Text('🛡️ Prevention:', style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF4A148C))),
          const SizedBox(height: 4),
          ...prevention.map((s) => Padding(padding: const EdgeInsets.only(left: 8, bottom: 2),
            child: Text('• $s', style: const TextStyle(fontSize: 13)))),
        ],

        if (rec.isNotEmpty) ...[
          const SizedBox(height: 12),
          Container(
            width: double.infinity, padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: const Color(0xFFEDE7F6), borderRadius: BorderRadius.circular(10)),
            child: Text('💡 $rec', style: const TextStyle(fontSize: 13, color: Color(0xFF4A148C))),
          ),
        ],
      ]),
    );
  }

  Widget _row(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 13)),
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
      ]),
    );
  }
}
