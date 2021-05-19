import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:rlp/Pages/GetPage.dart';
import 'package:rlp/Pages/PlacePage.dart';
import 'package:rlp/Pages/homePage.dart';
import 'package:rlp/Pages/listPage.dart';

class OptionPage extends StatelessWidget {
  static const routeName = '/optionPage';

  void obtenirImage(BuildContext context) async {
    final String url = 'http://10.0.2.2:5000/getObject.png';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));
    HttpClientResponse response = await request.close();
    //httpClient.close();
  }

  Future<bool> objectGrabbed(BuildContext context) async {
    final String url = 'http://10.0.2.2:5000/objectGrabbed';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();
    httpClient.close();
    if (jsonDecode(reply)['res'] == 'grabbed') {
     return true;
    } else {
      return false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: FloatingActionButton(
          onPressed: () {
            Navigator.of(context).pushNamed(HomePage.routeName);
          },
          elevation: 0,
          backgroundColor: Colors.orangeAccent,
          child: Icon(Icons.arrow_back),
        ),
        elevation: 0,
        backgroundColor: Colors.orangeAccent,
      ),
      backgroundColor: Colors.orangeAccent,
      body: Stack(
        children: <Widget>[
          Center(
            child: Container(
              width: 180,
              height: 250,
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
                      onPressed: () async{
                        obtenirImage(context);
                        var aux = await objectGrabbed(context);
                        if(!aux) {
                          Navigator.of(context).pushNamed(GetPage.routeName);
                        }
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
                      onPressed: () async{
                        obtenirImage(context);
                        var aux = await objectGrabbed(context);
                        if(aux) {
                          Navigator.of(context).pushNamed(PlacePage.routeName);
                        }

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
                        Navigator.of(context).pushNamed(ListPage.routeName);
                      }, //=> controlId(context),
                      child: Text(
                        'LIST OF OBJECTS',
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
