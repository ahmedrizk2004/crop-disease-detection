import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final String message;
  ApiException(this.message);
  @override
  String toString() => message;
}

class ApiService {
  static const String baseUrl = 'https://crop-disease-detection-production-9510.up.railway.app/api';
  static const _timeout = Duration(seconds: 60);

  static Map<String, dynamic> _handleResponse(http.Response res) {
    final body = jsonDecode(res.body);
    if (res.statusCode >= 200 && res.statusCode < 300) return body;
    throw ApiException(body['error'] ?? 'Server error (${res.statusCode})');
  }

  static Future<Map<String, dynamic>> _post(String path, Map<String, dynamic> data) async {
    try {
      final res = await http.post(
        Uri.parse('$baseUrl$path'),
        headers: {'Content-Type': 'application/json', 'ngrok-skip-browser-warning': 'true', 'bypass-tunnel-reminder': 'true'},
        body: jsonEncode(data),
      ).timeout(_timeout);
      return _handleResponse(res);
    } on SocketException {
      throw ApiException('❌ لا يوجد اتصال بالسيرفر\nتأكد أن الـ Backend شغال');
    } on TimeoutException {
      throw ApiException('⏱️ انتهت مدة الانتظار\nالسيرفر بطيء، حاول تاني');
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException('❌ خطأ غير متوقع: $e');
    }
  }

  static Future<Map<String, dynamic>> _get(String path) async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl$path'),
        headers: {'Content-Type': 'application/json', 'ngrok-skip-browser-warning': 'true', 'bypass-tunnel-reminder': 'true'},
      ).timeout(_timeout);
      return _handleResponse(res);
    } on SocketException {
      throw ApiException('❌ لا يوجد اتصال بالسيرفر\nتأكد أن الـ Backend شغال');
    } on TimeoutException {
      throw ApiException('⏱️ انتهت مدة الانتظار\nالسيرفر بطيء، حاول تاني');
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException('❌ خطأ غير متوقع: $e');
    }
  }

  static Future<Map<String, dynamic>> predictDisease(Map<String, dynamic> data) =>
      _post('/disease/predict', data);

  static Future<Map<String, dynamic>> predictYield(Map<String, dynamic> data) =>
      _post('/yield/predict', data);

  static Future<Map<String, dynamic>> analyzePlantData(
      String cropType, List<String> symptoms, Map<String, dynamic> conditions) =>
      _post('/ai/analyze-data', {
        'crop_type': cropType,
        'symptoms': symptoms,
        'conditions': conditions,
      });

  static Future<Map<String, dynamic>> analyzePlantImage(File imageFile) async {
    try {
      final bytes = await imageFile.readAsBytes();
      final b64 = base64Encode(bytes);
      return await _post('/ai/analyze-image', {'image_base64': b64});
    } on ApiException {
      rethrow;
    } catch (e) {
      throw ApiException('❌ خطأ في قراءة الصورة: $e');
    }
  }

  static Future<Map<String, dynamic>> getWeatherSummary() =>
      _get('/weather/summary');

  static Future<bool> checkHealth() async {
    try {
      final res = await http.get(
        Uri.parse('$baseUrl/health'),
      ).timeout(const Duration(seconds: 10));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
