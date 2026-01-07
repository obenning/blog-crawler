---
title: "Rechnungsversand per E-Mail: Neue Rechtslage nach OLG-Urteil"
author: ""
date: ""
url: "https://www.kerberos-compliance.com/wissen/blog/rechnungsversand-per-e-mail-neue-rechtslage-nach-olg-urteil"
excerpt: ""
crawled_at: "2026-01-07T03:44:33.630722"
---

# Rechnungsversand per E-Mail: Neue Rechtslage nach OLG-Urteil

**Autor:**   
**Datum:**   
**URL:** https://www.kerberos-compliance.com/wissen/blog/rechnungsversand-per-e-mail-neue-rechtslage-nach-olg-urteil

---

Veröffentlicht: 2025-03-25

Müssen sich die Maßnahmen zum Schutz personenbezogener Daten bei der Übermittlung per E-Mail ändern?

Müssen Rechnungen B2C künftig per Ende-zu-Ende-Verschlüsselung versendet werden?

Das jedenfalls legt eine Entscheidung des [OLG Schleswig-Holstein, Urteil vom 18. Dezember 2024(Az. 12 U 9/24)](https://www.gesetze-rechtsprechung.sh.juris.de/bssh/document/NJRE001598708) nahe.

Im zugrunde liegenden Fall hatte ein Bauunternehmer eine Rechnung mit einem Rechnungsbetrag von rund 15.000 € per E-Mail – lediglich per Transportverschlüsselung - an einen Verbraucher versendet. Aufgrund einer Manipulation der Rechnung (Betrugsmasche des sog. „Invoice Fraud“) zahlte jener an einen unbekannten Dritten. Die Parteien stritten vor Gericht darüber, ob der Unternehmer, seinen Lohn aus dem Bauvertrag vom Verbraucher trotz geleisteter Zahlung an den Dritten verlangen kann.

## Bauunternehmer bleibt wegen DSGVO-Verstößen auf Rechnung sitzen

Das OLG Schleswig-Holstein entschied, dass zwar die Zahlung des Verbrauchers an die Betrüger keine schuldbefreiende Wirkung gehabt habe. Dem Verbraucher stünde aber ein Schadensersatzanspruch aus Art. 82 DSGVO gegen den klagenden Bauunternehmer zu, weil dieser durch den „nur“ transportverschlüsselten Versand der Rechnungsmail seine Pflicht zum Schutz personenbezogener Daten gemäß Art. 32 DSGVO verletzt habe. Im Ergebnis blieb der Unternehmer damit auf seiner Rechnung sitzen.

Bislang wurde unter Berücksichtigung des Standes der Technik, der typischen Implementierungskosten und deren Verhältnis zu den Risiken einer Übermittlung personenbezogener Daten per E-Mail eine Differenzierung der Anforderungen an den Versand von E-Mail-Nachrichten in 3 Risiko-Gruppen unterschieden:

- Verpflichtungen bei normalen Risiken,
- bei hohem Risiko und
- bei Versand durch gesetzlich zur Verschwiegenheit Verpflichteten.
( [Orientierungshilfe der Konferenz der unabhängigen Datenschutzaufsichtsbehörden des Bundes und der Länder vom 27. Mai 2021](https://www.datenschutzkonferenz-online.de/media/oh/20210616_orientierungshilfe_e_mail_verschluesselung.pdf) )

Zudem wurde bislang für die Abschätzung des Risikos der Verarbeitung (Risikobewertung) die Eintrittswahrscheinlichkeit und die Schwere des möglichen Schadens betrachtet. ( [DSK Kurzpapier Nr. 18 Risiko für die Rechte und Freiheiten natürlicher Personen](https://www.datenschutzkonferenz-online.de/media/kp/dsk_kpnr_18.pdf) ).

Eine entsprechende Risikobewertung lässt das Urteil nicht erkennen. Es wurde vielmehr nur das finanzielle Risiko als ausschlaggebend angesehen. Es blieb auch ohne Belang, dass der Rechnungsempfänger nicht nur die Möglichkeit hatte, die Verarbeitung selbst zu prüfen (was im Rahmen einer Risikoanalyse Einfluss auf die Eintrittswahrscheinlichkeit hat), sondern die erhaltene Rechnung inhaltlich und äußerlich Anlass zur Prüfung geboten hatte. Im Rahmen einer Prüfung des Mitverschuldens klang dies zwar an, wurde jedoch im Ergebnis verneint.

Das Urteil des OLG Schleswig-Holstein wird - auch mit Blick auf die Umsetzbarkeit einer Ende-zu-Ende-Verschlüsselung im B2C-Geschäftskontakt - sehr kritisch gesehen. Da eine Ende-zu-Ende verschlüsselte E-Mail nur mit geeigneten technischen Mitteln geöffnet werden kann - wie OpenPGP (Pretty Good Privacy), S/MIME (Secure/Multipurpose Internet Mail Extensions) -, kann sie im B2C-Bereich nicht ohne weiteres als Standard genutzt werden.

Da das Urteil jedoch die Zeichen in Richtung höhere Sicherheitsanforderungen beim digitalen Rechnungsversand gestellt hat und damit die Risiken für Unternehmen aufgrund mangelnder Umsetzung technisch-organisatorischer Maßnahmen haften zu müssen gestiegen sind, wird man sich mit der Frage der sicheren Übermittlung von E-Mails auseinanderzusetzen haben.

## Risiken für Unternehmen sind gestiegen - TOMs notwendig

Neben der Erwägung technischer Maßnahmen zur Erhöhung der Sicherheit beim Rechnungsversand per E-Mail - wie Implementierung sicherer E-Mail-Verschlüsselung, Nutzung digitaler Signaturen und Versand über gesicherte Kundenportale - ist auch das Ergreifen zusätzlicher organisatorischer Maßnahmen eine Möglichkeit, ein dem Risiko angemessenes Schutzniveau zu gewährleisten.

Solche organisatorischen Maßnahmen könnten etwa sein:

- Bankverbindungen bei Änderungen über einen zweiten Kommunikationskanal (Telefon/Post) bestätigen ( Bankverbindungen verifizieren )
- Kunden über ihre Mitwirkungspflichten , Rechnungen auf Fälschungen zu überprüfen, informieren
- Kunden über Sicherheitsmaßnahme „Bankverbindung verifizieren“ informieren und im beidseitigen Interesse verpflichtende Rückfragen für Zweifelsfälle vorschreiben

## Hat das Urteil des OLG Schleswig-Holstein Auswirkungen auf den E-Mail-Versand B2B?

Konkrete gesetzliche Vorgaben für Sicherheitsvorkehrungen beim Versand von E-Mails im geschäftlichen Verkehr gibt es nicht und der sachliche Anwendungsbereich der Datenschutz-Grundverordnung ist nur für die Verarbeitung von Informationen eröffnet, die sich auf eine natürliche Person beziehen. Welches Maß an Sicherheitsvorkehrungen im konkreten B2B-Geschäft erwartet werden darf, bestimme sich nach den berechtigten Sicherheitserwartungen des Verkehrs unter Berücksichtigung der Zumutbarkeit (vgl. [Urteil des OLG Karlsruhe vom 27.07.2023, Az. 19 U 83/22](https://www.landesrecht-bw.de/bsbw/document/NJRE001546363) )

Im Zuge der steigenden Risiken beim E-Mail-Versand werden sich auch hier die Sicherheitserwartungen erhöhen. Insofern ist es kein Fehler, technisch-organisatorische Maßnahmen insgesamt zu überdenken. Im Geschäftskunden-Bereich und dort im Bereich der regelmäßig wiederkehrenden Vertragsleistungen ließen sich Risiken beim Rechnungsversand per E-Mail z.B. auch mittels Lastschriftverfahren minimieren.

Sie haben Fragen zu Ihren Sicherungsmaßnahmen? [Nehmen Sie jetzt Kontakt auf.](https://www.kerberos-compliance.com/unternehmen/kontakt)

Fatima Thönnes Manager GDPR Compliance
