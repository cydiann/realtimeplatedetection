import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('Binary Runner')),
        body: Center(
          child: ElevatedButton(
            onPressed: () {
              runBinary();
            },
            child: Text('Run Binary'),
          ),
        ),
      ),
    );
  }

  static const platform = MethodChannel('plaka_tanima_channel');

  void runBinary() async {
    try {
      final String result = await platform.invokeMethod('runBinary');
      print(result);
    } on PlatformException catch (e) {
      print("Failed to run binary: '${e.message}'.");
    }
  }
}
