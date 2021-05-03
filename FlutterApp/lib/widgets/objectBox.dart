import 'package:flutter/material.dart';

class ObjectBox extends StatelessWidget {
  final List<List<int>> llista;
  final String imageUrl;

  ObjectBox(this.llista, this.imageUrl);

  void sendPosition(BuildContext context) async {
    Navigator.of(context).pushNamed('/');
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Image(
          image: NetworkImage(imageUrl),
          height: 256,
          width: 256,
          fit: BoxFit.fill,
        ),
        ...(llista.map((element) {
          return Positioned(
            bottom: element[0] as double,
            right: element[1] as double,
            child: InkWell(
              onTap: () => sendPosition(context), //ALert do you want to get these object
              child: Container(
                width: 40,
                height: 40,
                color: Colors.white54,
              ),
            ),
          );
        })).toList(),
      ],
    );
  }
}
