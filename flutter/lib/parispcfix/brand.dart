import 'package:flutter/material.dart';

const bool parisPcFixEnabled =
    bool.fromEnvironment('PARISPCFIX', defaultValue: false);

class ParisPcFixBrand extends StatelessWidget {
  const ParisPcFixBrand({super.key, this.compact = false});

  final bool compact;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(
          horizontal: compact ? 6 : 14, vertical: compact ? 2 : 20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          RichText(
            text: TextSpan(
              style: TextStyle(
                  fontSize: compact ? 12 : 21,
                  fontWeight: FontWeight.w800,
                  color: const Color(0xFFE2EFFB)),
              children: const [
                TextSpan(text: 'PARISPC'),
                TextSpan(
                    text: 'FIX',
                    style: TextStyle(color: Color(0xFF00DCE7))),
              ],
            ),
          ),
          if (!compact)
            const Padding(
              padding: EdgeInsets.only(top: 7),
              child: Text('S E R V I C E   T O O L S',
                  style: TextStyle(
                      fontSize: 8,
                      color: Color(0xFFADC9DC),
                      letterSpacing: 1)),
            ),
        ],
      ),
    );
  }
}

class ParisPcFixBackdrop extends StatelessWidget {
  const ParisPcFixBackdrop({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    if (!parisPcFixEnabled) return child;
    return DecoratedBox(
      decoration: const BoxDecoration(
        image: DecorationImage(
          image: AssetImage('assets/parispcfix-night.png'),
          fit: BoxFit.cover,
        ),
      ),
      child: ColoredBox(color: const Color(0xAA031222), child: child),
    );
  }
}
