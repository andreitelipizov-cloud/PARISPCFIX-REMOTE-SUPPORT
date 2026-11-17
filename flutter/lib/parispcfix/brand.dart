import 'package:flutter/material.dart';

const bool parisPcFixEnabled =
    bool.fromEnvironment('PARISPCFIX', defaultValue: false);
const String parisPcFixEdition =
    String.fromEnvironment('PARISPCFIX_EDITION', defaultValue: '');

class ParisPcFixStyle {
  static const accent = Color(0xFF20E0D4);
  static const ink = Color(0xFF061423);
  static const muted = Color(0xFFA7BED0);
  static const border = Color(0x3336C7CE);

  static String text(BuildContext context, String key) {
    final language = Localizations.localeOf(context).languageCode;
    return (_copy[language] ?? _copy['en']!)[key]!;
  }

  static const _copy = {
    'en': {
      'subtitle': 'REMOTE SUPPORT',
      'client': 'CLIENT',
      'admin': 'TECHNICIAN',
      'workspace': 'Your support workspace',
      'detail': 'Connect. Diagnose. Resolve.'
    },
    'fr': {
      'subtitle': 'ASSISTANCE À DISTANCE',
      'client': 'CLIENT',
      'admin': 'TECHNICIEN',
      'workspace': 'Votre espace d’assistance',
      'detail': 'Connecter. Diagnostiquer. Résoudre.'
    },
    'ru': {
      'subtitle': 'УДАЛЁННАЯ ПОДДЕРЖКА',
      'client': 'КЛИЕНТ',
      'admin': 'СПЕЦИАЛИСТ',
      'workspace': 'Рабочее место специалиста',
      'detail': 'Подключение. Диагностика. Решение.'
    },
    'ro': {
      'subtitle': 'ASISTENȚĂ LA DISTANȚĂ',
      'client': 'CLIENT',
      'admin': 'TEHNICIAN',
      'workspace': 'Spațiul tău de asistență',
      'detail': 'Conectare. Diagnosticare. Rezolvare.'
    },
    'uk': {
      'subtitle': 'ВІДДАЛЕНА ПІДТРИМКА',
      'client': 'КЛІЄНТ',
      'admin': 'ФАХІВЕЦЬ',
      'workspace': 'Робоче місце фахівця',
      'detail': 'Підключення. Діагностика. Рішення.'
    },
  };
}

class ParisPcFixBrand extends StatelessWidget {
  const ParisPcFixBrand({super.key, this.compact = false});
  final bool compact;

  @override
  Widget build(BuildContext context) {
    if (compact) {
      return const Text.rich(
        TextSpan(children: [
          TextSpan(text: 'PARISPC'),
          TextSpan(
              text: 'FIX', style: TextStyle(color: ParisPcFixStyle.accent)),
        ]),
        style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w800,
            color: Color(0xFFF1F7FC),
            letterSpacing: 0.6),
      );
    }
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.fromLTRB(14, 18, 14, 16),
      padding: const EdgeInsets.fromLTRB(16, 20, 16, 18),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: ParisPcFixStyle.border),
        gradient: const LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xB31B4559), Color(0xC2081B2C)]),
        boxShadow: const [
          BoxShadow(
              color: Color(0x33000000), blurRadius: 24, offset: Offset(0, 8))
        ],
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(
          width: 46,
          height: 46,
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
              color: const Color(0xFF061728),
              borderRadius: BorderRadius.circular(13),
              border: Border.all(color: ParisPcFixStyle.border)),
          child: Image.asset('assets/parispcfix-icon.png'),
        ),
        const SizedBox(height: 18),
        const FittedBox(
            fit: BoxFit.scaleDown,
            alignment: Alignment.centerLeft,
            child: Text.rich(
                TextSpan(children: [
                  TextSpan(text: 'PARISPC'),
                  TextSpan(
                      text: 'FIX',
                      style: TextStyle(color: ParisPcFixStyle.accent)),
                ]),
                style: TextStyle(
                    fontSize: 27,
                    fontWeight: FontWeight.w800,
                    color: Color(0xFFF1F7FC),
                    letterSpacing: 0.6))),
        const SizedBox(height: 7),
        Text(ParisPcFixStyle.text(context, 'subtitle'),
            style: const TextStyle(
                fontSize: 9,
                letterSpacing: 1.2,
                fontWeight: FontWeight.w600,
                color: ParisPcFixStyle.muted)),
        if (parisPcFixEdition.isNotEmpty) ...[
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
                color: const Color(0x1920E0D4),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: ParisPcFixStyle.border)),
            child: Text(
                ParisPcFixStyle.text(context,
                    parisPcFixEdition == 'client' ? 'client' : 'admin'),
                style: const TextStyle(
                    color: ParisPcFixStyle.accent,
                    fontSize: 9,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1)),
          ),
        ],
      ]),
    );
  }
}

class ParisPcFixWorkspaceHeader extends StatelessWidget {
  const ParisPcFixWorkspaceHeader({super.key});

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.fromLTRB(24, 22, 24, 18),
        child: Row(children: [
          Expanded(
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                Text(ParisPcFixStyle.text(context, 'workspace'),
                    style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.w700,
                        color: Color(0xFFF1F7FC))),
                const SizedBox(height: 7),
                Text(ParisPcFixStyle.text(context, 'detail'),
                    style: const TextStyle(
                        fontSize: 12, color: ParisPcFixStyle.muted)),
              ])),
          const SizedBox(width: 12),
          const Icon(Icons.headset_mic_outlined,
              size: 30, color: ParisPcFixStyle.accent),
        ]),
      );
}

class ParisPcFixBackdrop extends StatelessWidget {
  const ParisPcFixBackdrop({super.key, required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) {
    if (!parisPcFixEnabled) return child;
    final theme = Theme.of(context);
    return DecoratedBox(
      decoration: const BoxDecoration(
        image: DecorationImage(
            image: AssetImage('assets/parispcfix-night.png'),
            fit: BoxFit.cover,
            alignment: Alignment.centerRight),
      ),
      child: DecoratedBox(
        decoration: const BoxDecoration(
            gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
              Color(0xB3061423),
              Color(0x70061423),
              Color(0xA3061423)
            ])),
        child: Theme(
          data: theme.copyWith(
            dividerColor: ParisPcFixStyle.border,
            inputDecorationTheme: theme.inputDecorationTheme.copyWith(
              filled: true,
              fillColor: const Color(0x66081425),
              focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10),
                  borderSide: const BorderSide(color: ParisPcFixStyle.accent)),
            ),
          ),
          child: child,
        ),
      ),
    );
  }
}
