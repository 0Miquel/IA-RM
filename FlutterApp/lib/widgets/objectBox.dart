import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';

import '../Exceptions.dart';

class ObjectBox extends StatelessWidget {
  final List<List<double>> llista;
  final String imageUrl;
  final double pi = 3.1415926535897932;

  ObjectBox({this.llista, this.imageUrl});

  showAlertDialog(BuildContext context, List<double> element) {
    Widget cancelButton = FlatButton(
      child: Text("NO"),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
    Widget continueButton = FlatButton(
      child: Text("YES"),
      onPressed: () => sendPosition(context, element),
    );

    AlertDialog alert = AlertDialog(
      title: Text("Get Object"),
      content: Text("Do you want to get the object?"),
      actions: [
        cancelButton,
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

  void sendPosition(BuildContext context, List<double> element) async {
    final Map jsonMap = {"posicio": element};
    //final String url = 'https://ia-rm-312715.oa.r.appspot.com/coppelia';
    final String url = 'http://127.0.0.1:5000/coppelia';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();
    //String reply = await response.transform(utf8.decoder).join();
    //httpClient.close();
  }

  _onTapDown(TapDownDetails details) {
    var x = details.globalPosition.dx;
    var y = details.globalPosition.dy;
    // or user the local position method to get the offset
    print(details.localPosition);
    print("tap down " + x.toString() + ", " + y.toString());
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(10.0),
          child: Image(
            image: NetworkImage(imageUrl),
            height: 512,
            width: 512,
            fit: BoxFit.fill,
          ),
        ),
        ...(llista.map((i) {
          return Positioned(
            top: i[0] - 168 / 2,
            left: i[1] - 47 / 2,
            child: Transform.rotate(
              angle: i[2] * -1,
              child: InkWell(
                onTap: () => showAlertDialog(context, i),
                onTapDown: (TapDownDetails details) => _onTapDown(details),
                //ALert do you want to get these object
                child: Container(
                  width: 47,
                  height: 168,
                  color: Colors.black45,
                ),
              ),
            ),
          );
        })).toList(),
      ],
    );
  }
}
