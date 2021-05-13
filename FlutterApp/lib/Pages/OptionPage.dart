import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:rlp/Pages/GetPage.dart';
import 'package:rlp/Pages/PlacePage.dart';

class OptionPage extends StatelessWidget {
  static const routeName = '/optionPage';
  void obtenirImage(BuildContext context) async {
    //final String url = 'https://ia-rm-312715.oa.r.appspot.com/coppelia';

    //final String url = 'https://ia-rm-312715.oa.r.appspot.com/coppelia';
    final String url = 'http://10.0.2.2:5000/getObject.png';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));

    HttpClientResponse response = await request.close();

    print(response.statusCode);
    httpClient.close();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.orangeAccent,
      ),
      backgroundColor: Colors.orangeAccent,
      body: Stack(
        children: <Widget>[
          Center(
            child: Container(
              width: 180,
              height: 190,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  SizedBox(
                    width: 180, // <-- match_parent
                    height: 70,
                    child: ElevatedButton(
                      style: ButtonStyle(
                        shape:
                            MaterialStateProperty.all<RoundedRectangleBorder>(
                          RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                        backgroundColor:
                            MaterialStateProperty.all(Colors.white),
                      ),
                      onPressed: () {
                        obtenirImage(context);
                        //sleep(Duration(seconds:5));
                        Navigator.of(context).pushNamed(GetPage.routeName);
                      }, //=> controlId(context),
                      child: Text(
                        'SELECT OBJECT',
                        style: TextStyle(
                          fontSize: 18,
                          color: HexColor('#FF7B02'),
                        ),
                      ),
                    ),
                  ),
                  SizedBox(
                    width: 180, // <-- match_parent
                    height: 70,
                    child: ElevatedButton(
                      style: ButtonStyle(
                        shape:
                            MaterialStateProperty.all<RoundedRectangleBorder>(
                          RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                        backgroundColor:
                            MaterialStateProperty.all(Colors.white),
                      ),
                      onPressed: () {
                        Navigator.of(context).pushNamed(PlacePage.routeName);
                      }, //=> controlId(context),
                      child: Text(
                        'PLACE OBJECT',
                        style: TextStyle(
                          fontSize: 18,
                          color: HexColor('#FF7B02'),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
