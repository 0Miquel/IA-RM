import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_image_map/flutter_image_map.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:path/path.dart';
import 'package:rlp/Pages/homePage.dart';
import 'package:rlp/widgets/objectBox.dart';

class GetPage extends StatelessWidget {
  static const routeName = '/getPage';
  final String imageUrl = 'http://127.0.0.1:5000/getObject.png';

  GetPage() {

    //pillar imatge i llista

  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('GET OBJECT'),
      ),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.all(20),
            child: ObjectBox([
              [10, 200],
              [200, 200]
            ], imageUrl),
          ),
        ],
      ),
    );
  }
}
