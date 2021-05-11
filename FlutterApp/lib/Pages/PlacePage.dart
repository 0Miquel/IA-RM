import 'package:flutter/material.dart';

class PlacePage extends StatelessWidget {
  static const routeName = '/placePage';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Place OBJECT'),
      ),
      body: Center(
        child: Text('get ui'),
      ),
    );
  }
}
