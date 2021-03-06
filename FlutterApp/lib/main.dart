import 'package:flutter/material.dart';
import 'package:rlp/Pages/GetPage.dart';
import 'package:rlp/Pages/OptionPage.dart';
import 'package:rlp/Pages/listPage.dart';
import 'Pages/PlacePage.dart';
import 'Pages/homePage.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IA-RM',
      theme: ThemeData(
        primarySwatch: Colors.orange,
        canvasColor: Colors.orangeAccent,
      ),
      initialRoute: '/',
      routes: {
        '/': (ctx) => HomePage(),
        OptionPage.routeName: (ctx) => OptionPage(),
        GetPage.routeName: (ctx) => GetPage(),
        PlacePage.routeName: (ctx) => PlacePage(),
        ListPage.routeName: (ctx) => ListPage(),
      },
    );
  }
}
