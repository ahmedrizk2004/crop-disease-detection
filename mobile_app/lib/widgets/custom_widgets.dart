import 'package:flutter/material.dart';

class LoadingWidget extends StatelessWidget {
  final Color color;
  const LoadingWidget({super.key, this.color = const Color(0xFF2E7D32)});
  @override
  Widget build(BuildContext context) => Center(child: CircularProgressIndicator(color: color));
}

class ErrorWidget2 extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;
  const ErrorWidget2({super.key, required this.message, this.onRetry});
  @override
  Widget build(BuildContext context) => Center(
    child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      const Icon(Icons.error_outline, color: Colors.red, size: 48),
      const SizedBox(height: 12),
      Text(message, style: const TextStyle(color: Colors.red), textAlign: TextAlign.center),
      if (onRetry != null) ...[const SizedBox(height: 12), ElevatedButton(onPressed: onRetry, child: const Text('Retry'))],
    ]),
  );
}
