import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:rlp/Pages/OptionPage.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatelessWidget {
  final myController = TextEditingController();

  void controlId(BuildContext context) async {
    /*
    final url = Uri.http('127.0.0.1:5000', '/coppelia');
    final response = await http.post(url,
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: '{"coppeliaid": "19999"}'
    );

    print(response.body);
    */
    //if(jsonDecode(response.body)['res']  == 'ok') {
      Navigator.of(context).pushNamed(OptionPage.routeName);
  //  }else{
   //   print('f');
    //slatar alerta canviar id
   // }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Coppelia Id',
            ),
            TextField(
              controller: myController,
              decoration: InputDecoration(
                  border: OutlineInputBorder(), hintText: 'Enter id here...'),
            ),
            ElevatedButton(
              onPressed: () => controlId(context),
              child: Text('START'),
            )
          ],
        ),
      ),
    );
  }
}
