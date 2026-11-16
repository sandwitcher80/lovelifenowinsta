# Redaktions-Playbook @jens.lovelifenow (LoveLifeNow)

Ziel: In wenigen Wochen mehr NEUE Follower durch Karussells. Keine Garantie, aber alles auf Reichweite, Speichern und Teilen optimiert.
Sprache: Deutsch, du-Ansprache, warm, kurz, keine Heilversprechen. Quelle auf Slides nur "@jens.lovelifenow" (kein Podcast-Hinweis).

## Marke
Royalblau #2D5AAA, Blush #F8EEE8, Navy #1B3470, Hellblau #DCE6F5, weisses Hoehenlinien-Muster, runde Sans, kursive Serif im Button.
Rendern: `python3 tools/render.py specs/<datum-slug>.json` (siehe Docstring in tools/render.py). Pattern-Offset `start` je Post um 6 erhoehen (letzter Wert in calendar.md).
Layout je Woche variieren: Schritt-Karussell, Mythos/Fakt, Checkliste mit 01/02/03, Einzelzitat in Serif, grosse Frage, Palette wechseln (BL/BS, NV/LB), Muster zoomen.

## Themen (Rotation)
Breathwork, Hypnose, luzides Traeumen, Achtsamkeit/Gefuehle, Nervensystem/Stress, Impro/Leichtigkeit ("Ja, und"), Schlaf, Lampenfieber, Persoenliches (nur mit Fotos/Geschichten von Jens). Events (Sessions, Erstgespraech) hoechstens jeder 4.-5. Beitrag als Haupt-CTA, sonst 1 Zeile in der Caption.
Inhalte stammen aus Jens' Podcast-Transkripten (Original nur lokal, nicht im Repo) und eigenem Wissen. Keine medizinischen Versprechen. Bei Breathwork: Hinweis "intensive Techniken begleitet, bei gesundheitlichen Fragen aerztlich klaeren". Hypnose: "ersetzt keine Therapie".

## Rhythmus
3 Posts/Woche: Mo 10:30, Mi 10:00, Fr 10:00 (Europe/Berlin). Beste Zeiten laut Metricool: Mi/Do/Fr 10:00, Mo 10-11, zweitens ca. 18:00.
Immer mind. 14 Tage Vorlauf als Entwurf in Metricool (Brand 8126656, Instagram, draft:true, instagramData.type POST).

## Post-Ready-Checkliste (jeden Entwurf pruefen)
1. Slide 1: Haken in max. ~10 Woertern (Frage, Mythos, Nutzen, Zahl), lesbar als Thumbnail. Kein Logo-Gedoens.
2. 5-8 Slides, 1 Gedanke pro Slide, max. ~25 Woerter, Text nicht am Rand abgeschnitten (Contact-Sheet ansehen).
3. Vorletzter/letzter Slide: Mehrwert-Zusammenfassung + klarer CTA: Speichern, Teilen ("schick es jemandem, der ..."), Kommentar-Frage, in jedem 2. Post "Folge @jens.lovelifenow fuer mehr".
4. Caption: Zeile 1 = Haken mit Schluesselbegriff (wird in der Vorschau gelesen, auch Suchbegriff), dann 2-4 kurze Absaetze, Kommentarfrage, optionaler Event-Hinweis, am Ende 5-8 passende Hashtags (gemischt gross/klein, kein #fyp-Spam).
5. Kein Kauderwelsch, keine Tippfehler in Hashtags, Umlaute korrekt, Datumsangaben stimmen (Event: Breathwork Session "Weck deine Energie", So 29.11.2026 11:00, Improtheater Mannheim).
6. Alt-Text pro Slide (mediaAltText) mit dem Slide-Text setzen (Barrierefreiheit + Suche).
7. Ersten Kommentar (firstCommentText) fuer zusaetzliche Hashtags/Frage nutzen, wenn sinnvoll.
8. Nie draft:false setzen, ausser Jens gibt ausdruecklich frei.

## Lernschleife
Montags: Metricool-Analytics der letzten 7/30 Tage ziehen (Reichweite, Saves, Shares, Follower-Zuwachs je Post). Gewinner-Hooks/Layouts/Themen in calendar.md unter "Learnings" festhalten und die Planung danach ausrichten (mehr von dem, was gespeichert/geteilt wird).

## Git
Commit-Trailer: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` und `Claude-Session: <aktuelle Session-URL>`. Bilder oeffentlich via raw.githubusercontent.com/sandwitcher80/lovelifenowinsta/main/posts/<ordner>/slide_N.png.
