import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
    return MaterialApp(
      debugShowCheckedModeBanner: true,
      theme: ThemeData.dark(),
      title: "RAG Assistant",
      home: RAGHomeScreen(),
    );
  }
}

class RAGHomeScreen extends StatefulWidget {
  // INIT the class
  const RAGHomeScreen({super.key});

  // The build method
  @override
  State<RAGHomeScreen> createState() => _RAGHomeScreenState();
}

class _RAGHomeScreenState extends State<RAGHomeScreen> {
  // Fields of teh calss
  final TextEditingController _myController = TextEditingController();
  final String _backendUrl = const String.fromEnvironment(
    "BACKEND_URL",
    defaultValue: "http://localhost:8000",
  );
  String _answer = "";

  @override
  void dispose() {
    _myController.dispose();
    super.dispose();
  }

  // Send data on press
  Future<void> sendDataOnButtonPress() async {
    // Get the data
    final textToSend = _myController.text;

    // Guard Clause
    if (textToSend.isEmpty) return;

    // For chrome and web
    try {
      // Sanitize the Text for URL
      final encodedText = Uri.encodeFull(textToSend);
      // Create a URI object
      final url = Uri.parse(
        "$_backendUrl/api/rag/ask?question=$encodedText&collection_name=DEFAULT_COLLECTIONS",
      );
      print("Sending data....$url");

      // Get response
      final response = await http.post(url);

      if (response.statusCode == 200) {
        //The response is successfull
        final data = jsonDecode(response.body);
        // Wrap the conditional actions in a setsate
        setState(() {
          // Get the answer from the data
          _answer = data["answer"].toString();
          // Clear the controller
          _myController.clear();
        });
      } else {
        print("Error Sending data: ${response.statusCode}}");
      }
    } catch (e) {
      print("Connection error: $e");
      print("Tip: Is your FastAPI server actually running?");
    }
  }

  // The
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const Text(
              "RAG Assistant",
              style: TextStyle(
                fontSize: 34,
                fontWeight: FontWeight.bold,
                color: Colors.amber,
              ),
            ),
            const Text("Enter your question here:"),
            Padding(
              padding: const EdgeInsets.all(20.0),
              child: SizedBox(
                height: 500.0,
                width: 1000,
                child: TextField(
                  // --- LINKING THE EAR ---
                  controller: _myController,
                  maxLength: null,
                  minLines: null,
                  maxLines: null,
                  expands: true,
                  textAlignVertical: TextAlignVertical.top,
                  decoration: InputDecoration(
                    hintText: "Please enter your question here.",
                    border: OutlineInputBorder(),
                    filled: true,
                    fillColor: Colors.blueGrey[900],
                  ),
                ),
              ),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.amber,
                foregroundColor: Colors.black,
              ),
              onPressed: sendDataOnButtonPress,
              child: const Text("Ask your expert!!"),
            ),
            // The Conditional Answer widget
            if (_answer.isNotEmpty)
              Padding(
                padding: const EdgeInsets.all(25.0),
                child: Container(
                  width: 1000,
                  padding: const EdgeInsets.all(15),
                  decoration: BoxDecoration(
                    color: Colors.blueGrey[800],
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                      color: Colors.amber.withValues(alpha: 0.5),
                    ),
                  ),
                  child: Text(
                    "AI Answer $_answer",
                    style: const TextStyle(fontSize: 16, color: Colors.white70),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
