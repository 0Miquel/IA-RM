import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:rlp/Pages/OptionPage.dart';


class PlaceObjectBox extends StatelessWidget {
  final String imageUrl;

  PlaceObjectBox({this.imageUrl});

  showAlertDialog(BuildContext context, TapDownDetails details) {
    Widget cancelButton = FlatButton(
      child: Text("NO"),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
    Widget continueButton = FlatButton(
      child: Text("YES"),
      onPressed: () => sendPosition(
          context, [details.localPosition.dy, details.localPosition.dx]),
    );

    AlertDialog alert = AlertDialog(
      title: Text("Place Object"),
      content: Text("Do you want to place the object?"),
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
  showAlertDialogNotAPlace(BuildContext context) {
    Widget continueButton = FlatButton(
      child: Text("Continue"),
      onPressed: () {Navigator.of(context).pop();},
    );

    AlertDialog alert = AlertDialog(
      title: Text("Error"),
      content: Text("Cannot place an objecte here, please choose a place"),
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
  void sendPosition(BuildContext context, List<double> element) async {

    double x = element[0] * 512 /(MediaQuery.of(context).size.width - 60);
    double y = element[1] * 512 /(MediaQuery.of(context).size.width - 60);

    final Map jsonMap = {"x": x, "y": y};
    final String url = 'http://10.0.2.2:5000/placeObject';
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
      Navigator.of(context).pop();
      showAlertDialogNotAPlace(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    imageCache.clear();
    return Stack(
      children: [
        Positioned(
          top: 0,
          left: 0,
          child: Image(
            image: NetworkImage(imageUrl),
            key: ValueKey(imageUrl),
            height: MediaQuery.of(context).size.width - 60,
            width: MediaQuery.of(context).size.width - 60,
            //fit: BoxFit.contain,
          ),
        ),

        InkWell(
          onTap: () => {},
          onTapDown: (TapDownDetails details) {
            showAlertDialog(context, details);
          },

          child: Container(
            width: 512,
            height: MediaQuery.of(context).size.width-60,
            color: Colors.black12,
          ),
        ),

      ],
    );
  }
}
