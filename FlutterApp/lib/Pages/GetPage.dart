import 'package:flutter/material.dart';
import 'package:rlp/widgets/GetObjectBox.dart';
import 'OptionPage.dart';

class GetPage extends StatelessWidget {
  static const routeName = '/getPage';
  final String imageUrl = 'http://10.0.2.2:5000/getObject.png';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: FloatingActionButton(
          onPressed: () {
            Navigator.of(context).pushNamed(OptionPage.routeName);
          },
          elevation: 0,
          backgroundColor: Colors.orangeAccent,
          child: Icon(Icons.arrow_back),
        ),
        backgroundColor: Colors.orangeAccent,
        title: Text('GET OBJECT'),
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
                child: GetObjectBox(
                  imageUrl: imageUrl,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
