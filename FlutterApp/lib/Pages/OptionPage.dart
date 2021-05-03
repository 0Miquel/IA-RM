import 'package:flutter/material.dart';
import 'package:rlp/Pages/GetPage.dart';
import 'package:rlp/Pages/PlacePage.dart';

class OptionPage extends StatelessWidget {
  static const routeName = '/optionPage';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pushNamed(GetPage.routeName);
              },
              child: Text('SELECT OBJECT'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).pushNamed(PlacePage.routeName);
              },
              child: Text('PLACE OBJECT'),
            ),
            FloatingActionButton(onPressed: (){
              Navigator.of(context).pop();
            })
          ],
        ),
      ),
    );
  }
}