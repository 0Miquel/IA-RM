import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:rlp/widgets/PlaceObjectBox.dart';
import 'package:rlp/widgets/objectBox.dart';

class PlacePage extends StatelessWidget {
  static const routeName = '/placePage';
  //final String imageUrl = 'https://ia-rm-313007.oa.r.appspot.com/getObject.png';
  final String imageUrl = 'http://10.0.2.2:5000/getObject.png';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.orangeAccent,
        title: Text('PLACE OBJECT'),
        elevation: 0,
      ),
      body: Padding(
        padding: EdgeInsets.all(10),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.all(Radius.circular(20)),
          ),
          child: Column(
            children: [
              Padding(
                padding: EdgeInsets.all(20),
                child: PlaceObjectBox(imageUrl:imageUrl),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
