import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  // Init the class
  const MyApp({super.key});

  // the build
  @override
  Widget build(BuildContext context) {
    // The base of the app
    return MaterialApp(debugShowCheckedModeBanner: true);
  }
}
