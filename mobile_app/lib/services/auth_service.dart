import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const _timeout = Duration(seconds: 30);
  static const _base = 'http://192.168.1.21:5000/api/auth';

  static Future<Map<String, dynamic>> register(String name, String email, String password) async {
    try {
      final res = await http.post(
        Uri.parse(_base + '/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'name': name, 'email': email, 'password': password}),
      ).timeout(_timeout);
      final body = jsonDecode(res.body);
      if (res.statusCode == 201) {
        await _saveSession(body['token'], body['user']);
        return {'success': true, 'user': body['user']};
      }
      return {'success': false, 'error': body['error'] ?? 'Registration failed'};
    } on TimeoutException {
      return {'success': false, 'error': 'Connection timeout. Try again.'};
    } catch (e) {
      return {'success': false, 'error': 'Connection error: ' + e.toString()};
    }
  }

  static Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final res = await http.post(
        Uri.parse(_base + '/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      ).timeout(_timeout);
      final body = jsonDecode(res.body);
      if (res.statusCode == 200) {
        await _saveSession(body['token'], body['user']);
        return {'success': true, 'user': body['user']};
      }
      return {'success': false, 'error': body['error'] ?? 'Login failed'};
    } on TimeoutException {
      return {'success': false, 'error': 'Connection timeout. Try again.'};
    } catch (e) {
      return {'success': false, 'error': 'Connection error: ' + e.toString()};
    }
  }

  static Future<Map<String, dynamic>> resetPassword(String email, String newPassword) async {
    try {
      final res = await http.post(
        Uri.parse(_base + '/reset-password'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'new_password': newPassword}),
      ).timeout(_timeout);
      final body = jsonDecode(res.body);
      if (res.statusCode == 200) return {'success': true};
      return {'success': false, 'error': body['error'] ?? 'Reset failed'};
    } on TimeoutException {
      return {'success': false, 'error': 'Connection timeout. Try again.'};
    } catch (e) {
      return {'success': false, 'error': 'Connection error: ' + e.toString()};
    }
  }

  static Future<void> _saveSession(String token, Map user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', token);
    await prefs.setString('user', jsonEncode(user));
  }

  static Future<Map<String, dynamic>?> getUser() async {
    final prefs = await SharedPreferences.getInstance();
    final u = prefs.getString('user');
    return u != null ? jsonDecode(u) : null;
  }

  static Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('token');
  }

  static Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null && token.isNotEmpty;
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    await prefs.remove('user');
  }
}