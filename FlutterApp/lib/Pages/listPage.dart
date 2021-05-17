import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:rlp/widgets/listOfObjects.dart';
import 'OptionPage.dart';

class ListPage extends StatefulWidget {
  static const routeName = '/listPage';
  var llista;

  ListPage({this.llista});

  @override
  _ListPageState createState() => _ListPageState();
}

class _ListPageState extends State<ListPage> {
  List<String> llista = ['loading'];

  Future<bool> getListOfObjects() async {
    final String url = 'http://10.0.2.2:5000/listObjects';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.getUrl(Uri.parse(url));
    HttpClientResponse response = await request.close();
    var reply = await response.transform(utf8.decoder).join();
    var res1 = jsonDecode(reply)['list'];
    List<String> res = res1 != null ? List.from(res1) : null;

    setState(() {
      llista = res;
    });

    httpClient.close();
  }
  void initState() {
    super.initState();
    getListOfObjects();
  }

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
        title: Text('SELECT OBJECT'),
        elevation: 0,
        backgroundColor: Colors.orangeAccent,
      ),
      backgroundColor: Colors.orangeAccent,
      body: Padding(
        padding: EdgeInsets.all(10),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.all(Radius.circular(20)),
          ),
          child: ListOfObjects(llista)
        ),
      ),
    );
  }
}
