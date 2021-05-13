import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:rlp/Pages/OptionPage.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatelessWidget {
  final myController = TextEditingController();
  showAlertDialog(BuildContext context) {

    Widget continueButton = FlatButton(
      child: Text("Ok"),
      onPressed: () { Navigator.of(context).pop();},
    );

    AlertDialog alert = AlertDialog(
      title: Text("Error"),
      content: Text("Unable to connect!"),
      actions: [
        continueButton,
      ],
    );
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return alert;
      },
    );
  }
  void controlId(BuildContext context) async {
    final Map jsonMap = {"coppeliaid": myController.text};
    //final String url = 'https://ia-rm-313007.oa.r.appspot.com/coppelia';
    final String url = 'http://10.0.2.2:5000/coppelia';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();
    httpClient.close();

    if (jsonDecode(reply)['res'] == 'ok') {

      Navigator.of(context).pushNamed(OptionPage.routeName);
    } else {
      showAlertDialog(context);
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      body: Container(
        /*
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
            colors: [
              HexColor('#FF7B02'),
              HexColor('#FFCB52'),
            ],
          ),
        ),
        */
        child: Center(
          child: Container(
            width: 300,
            height: 330,
            child: Padding(
              padding:
                  EdgeInsets.only(left: 30, right: 30, bottom: 10, top: 10),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  Text(
                    'IA-RM',
                    style: TextStyle(
                      fontSize: 30,
                      color: Colors.black,
                    ),
                  ),

                    TextField(
                      controller: myController,
                      style: TextStyle(
                        color: Colors.black,
                        height: 1.5,
                      ),
                      decoration: InputDecoration(
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(30),
                          borderSide: BorderSide.none,
                        ),

                        hintText: 'Enter Coppelia Id',
                        filled: true,
                        contentPadding: EdgeInsets.all(20),
                        fillColor: Colors.black12//HexColor('#d87e2c'), //'#d87e2c'),
                      ),
                    ),

                  SizedBox(
                    width: double.infinity, // <-- match_parent
                    height: 60,

                    child: ElevatedButton(
                      style: ButtonStyle(
                        shape:
                            MaterialStateProperty.all<RoundedRectangleBorder>(
                          RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(30),
                          ),
                        ),
                        backgroundColor:
                            MaterialStateProperty.all(Colors.white),
                      ),
                      onPressed: () {controlId(context);},//=> controlId(context),
                      child: Text(
                        'START',
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
        ),
      ),
    );
  }
}
