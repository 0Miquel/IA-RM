import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_image_map/flutter_image_map.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:path/path.dart';
import 'package:rlp/Pages/homePage.dart';
import 'package:rlp/widgets/GetObjectBox.dart';
import 'package:rlp/widgets/PlaceObjectBox.dart';
import 'package:rlp/widgets/objectBox.dart';

class GetPage extends StatelessWidget {
  static const routeName = '/getPage';

  //final String imageUrl = 'https://ia-rm-313007.oa.r.appspot.com/getObject.png';
  final String imageUrl = 'http://10.0.2.2:5000/getObject.png';
  //List<dynamic> llista;

/*
  void obtenirPage(BuildContext context) async {
    //final String url = 'https://ia-rm-312715.oa.r.appspot.com/coppelia';
    final Map jsonMap = {"x": 12, "y": 20};
    //final String url = 'https://ia-rm-312715.oa.r.appspot.com/coppelia';
    final String url = 'http://127.0.0.1:5000/coppelia';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();
    httpClient.close();

    if (jsonDecode(reply)['res'] == 'ok') {
      //Navigator.of(context).pushNamed(OptionPage.routeName);
    } else {
      //Navigator.of(context).pushNamed(OptionPage.routeName);
      print('f');
      //slatar alerta canviar id
    }
    //httpClient.close();
  }


  Future<http.Response> f2(BuildContext context) async {
    final response = await http.get(Uri.http('127.0.0.1:5000', '/getObject'));
    var resp = jsonDecode(response.body);
    llista = resp != null ? List.from(resp) : null;
  }
  */

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
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
                /*
                ObjectBox( //TODO mirar future builder -> senvia llista abasn qeu acabi http i sta coma null
                  llista: [[325,412,-0.74, 168, 47]],
                  imageUrl: imageUrl,
                ),
              */
              ),
            ],
          ),
        ),
      ),
    );
  }
}
