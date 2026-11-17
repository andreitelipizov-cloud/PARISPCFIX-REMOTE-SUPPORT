import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_hbb/parispcfix/brand.dart';

void main() {
  testWidgets('Client branding fits a narrow window in all five languages',
      (tester) async {
    for (final language in ['ru', 'fr', 'ro', 'uk', 'en']) {
      await tester.pumpWidget(MaterialApp(
        home: Builder(
            builder: (context) => Localizations.override(
                  context: context,
                  locale: Locale(language),
                  child: const Scaffold(
                      body: Align(
                    alignment: Alignment.topLeft,
                    child: SizedBox(width: 320, child: ParisPcFixBrand()),
                  )),
                )),
      ));
      await tester.pumpAndSettle();
      expect(
          find.textContaining('PARISPC', findRichText: true), findsOneWidget);
      expect(tester.takeException(), isNull, reason: language);
    }
  });

  testWidgets('Compact branding fits the desktop title bar', (tester) async {
    await tester.pumpWidget(const MaterialApp(
        home: Scaffold(
      body: SizedBox(
          width: 130, height: 30, child: ParisPcFixBrand(compact: true)),
    )));
    await tester.pumpAndSettle();
    expect(find.textContaining('PARISPC', findRichText: true), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
