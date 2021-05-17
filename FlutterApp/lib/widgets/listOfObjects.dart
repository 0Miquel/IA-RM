import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:rlp/Pages/PlacePage.dart';

class ListOfObjects extends StatelessWidget {
  var llista;
   ListOfObjects(this.llista);

  void sendPosition(BuildContext context, String name) async {
    final Map jsonMap = {"object": name};
    final String url = 'http://10.0.2.2:5000/listObjectSend';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();
    httpClient.close();

    if (jsonDecode(reply)['res'] == 'ok') {
      Navigator.of(context).pushNamed(PlacePage.routeName);
    }
  }
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(15),
      children: <Widget>[
        ...(llista.map((name) {
          return Card(
            child: SizedBox(
              width: 330, // <-- match_parent
              height: 70,
              child: InkWell(
                onTap: () {
                  sendPosition(context, name);
                }, //=> controlId(context),
                child: Center(
                  child: Container(
                    width: MediaQuery.of(context).size.width - 60,
                    height: MediaQuery.of(context).size.width - 60,
                    //color: Colors.black12,
                    decoration: BoxDecoration(
                      // border: Border.all(color: Colors.black),
                      borderRadius: BorderRadius.all(Radius.circular(20)),
                    ),
                    child: Center(
                      child: Text(
                        name.toUpperCase(),
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 18,
                          color: HexColor('#FF7B02'),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          );
        })).toList()
      ],
    );
  }
}
