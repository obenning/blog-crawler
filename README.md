# Blog Content Crawler für Claude AI

Dieses Repository crawlt automatisch alle Blog-Artikel von deiner Squarespace-Website und speichert sie als strukturierte Markdown-Dateien. Die Inhalte können dann direkt an Claude AI als Wissensgrundlage übergeben werden.

## 🎯 Zweck

- **Automatisches Crawling:** Alle Blog-Artikel werden regelmäßig gecrawlt
- **Strukturierte Speicherung:** Artikel werden als Markdown mit Metadaten gespeichert
- **Claude-kompatibel:** Inhalte sind optimiert für die Nutzung mit Claude AI
- **Versionskontrolle:** Alle Änderungen werden in Git getrackt

## 🚀 Setup

### 1. Repository erstellen

```bash
# Neues Repository auf GitHub erstellen
# Dann lokal klonen
git clone https://github.com/DEIN-USERNAME/blog-crawler.git
cd blog-crawler
```

### 2. Konfiguration anpassen

Öffne `blog_crawler.py` und passe die BASE_URL an (Zeile ~270):

```python
BASE_URL = "https://www.kerberos-compliance.com/wissen/blog"  # Deine URL hier
```

### 3. Lokaler Test

```bash
# Dependencies installieren
pip install -r requirements.txt

# Crawler manuell ausführen
python blog_crawler.py
```

Die gecrawlten Artikel befinden sich dann im Ordner `blog_content/`.

### 4. Auf GitHub pushen

```bash
git add .
git commit -m "Initial setup"
git push
```

### 5. GitHub Actions aktivieren

Der Workflow läuft automatisch:
- **Täglich um 2:00 Uhr UTC**
- **Bei jedem Push** (für Testing)
- **Manuell über GitHub Actions Tab**

## 📁 Struktur

```
.
├── .github/
│   └── workflows/
│       └── crawl-blog.yml      # GitHub Actions Workflow
├── blog_content/               # Gecrawlte Artikel (wird erstellt)
│   ├── artikel-1.md
│   ├── artikel-2.md
│   ├── index.json             # Index aller Artikel
│   └── README.md              # Übersicht der Artikel
├── blog_crawler.py            # Haupt-Crawler-Script
├── requirements.txt           # Python Dependencies
└── README.md                  # Diese Datei
```

## 🔧 Konfiguration

### Crawling-Zeitplan ändern

Bearbeite `.github/workflows/crawl-blog.yml`:

```yaml
schedule:
  # Täglich um 2:00 Uhr
  - cron: '0 2 * * *'
  
  # Jede Stunde
  # - cron: '0 * * * *'
  
  # Jeden Montag um 8:00 Uhr
  # - cron: '0 8 * * 1'
```

### Output-Verzeichnis ändern

In `blog_crawler.py`:

```python
OUTPUT_DIR = "blog_content"  # Anpassen
```

## 📖 Nutzung mit Claude AI

### Option 1: Einzelne Dateien hochladen

1. Gehe zu `blog_content/` in deinem Repository
2. Lade die benötigten `.md` Dateien herunter
3. Uploade sie zu Claude mit deiner Anfrage

### Option 2: Gesamtes Archiv nutzen

```bash
# Alle Artikel in eine Datei kombinieren
cd blog_content
cat *.md > alle_artikel.md
```

Dann `alle_artikel.md` zu Claude hochladen.

### Option 3: GitHub Raw Links

Du kannst Claude direkt auf die Raw-Dateien verweisen:

```
https://raw.githubusercontent.com/DEIN-USERNAME/blog-crawler/main/blog_content/artikel-name.md
```

## 🔍 Was wird gecrawlt?

Für jeden Artikel wird extrahiert:

- **Titel**
- **Autor**
- **Datum**
- **Excerpt/Zusammenfassung**
- **Vollständiger Content**
- **URL zum Original**
- **Crawling-Zeitstempel**

## 📊 Monitoring

### Status überprüfen

1. Gehe zu deinem Repository auf GitHub
2. Klicke auf "Actions"
3. Sieh dir die Workflow-Runs an

### Manuell triggern

1. Gehe zu "Actions" Tab
2. Wähle "Crawl Blog Content"
3. Klicke "Run workflow"

### Fehler beheben

Logs findest du unter:
- GitHub Actions → Workflow Run → Job Details

## 🛠️ Erweiterte Features

### Nur neue Artikel crawlen

Standardmäßig werden alle Artikel neu gecrawlt. Um dies zu optimieren, kannst du in `blog_crawler.py` eine Prüfung einbauen:

```python
def should_crawl(self, url, filepath):
    """Prüfe ob Artikel neu gecrawlt werden muss"""
    if filepath.exists():
        # Prüfe Alter der Datei
        age_days = (datetime.now() - datetime.fromtimestamp(filepath.stat().st_mtime)).days
        if age_days < 7:  # Nicht älter als 7 Tage
            return False
    return True
```

### Benachrichtigungen einrichten

Füge zu `.github/workflows/crawl-blog.yml` hinzu:

```yaml
    - name: Send notification
      if: success()
      uses: someaction/notification@v1
      with:
        message: "Blog crawling completed: ${{ steps.git-check.outputs.changed }}"
```

## 📝 Best Practices für Claude

### Kontextgröße beachten

Claude hat ein Kontextfenster. Bei vielen Artikeln:

1. **Nutze den Index:** `blog_content/index.json` zeigt alle Artikel
2. **Filtere nach Thema:** Lade nur relevante Artikel hoch
3. **Nutze Excerpts:** Für Überblick erst die Zusammenfassungen

### Prompt-Beispiele

```
Ich habe dir alle Blog-Artikel aus blog_content/ zur Verfügung gestellt. 
Beantworte folgende Frage basierend auf diesen Artikeln: [FRAGE]
```

```
Durchsuche die Blog-Artikel nach Informationen zu [THEMA] und erstelle 
eine Zusammenfassung der wichtigsten Punkte.
```

```
Vergleiche die verschiedenen Artikel zum Thema [THEMA] und zeige mir 
die Entwicklung der Meinungen/Informationen über die Zeit.
```

## 🔒 Sicherheit

- **Keine sensiblen Daten:** Der Crawler speichert nur öffentliche Blog-Inhalte
- **Rate Limiting:** 1 Sekunde Pause zwischen Requests
- **Robots.txt:** Respektiert Squarespace Richtlinien

## 🐛 Troubleshooting

### "No blog posts found"

- Überprüfe die BASE_URL
- Stelle sicher, dass die HTML-Struktur von Squarespace sich nicht geändert hat
- Teste den Crawler lokal mit `python blog_crawler.py`

### GitHub Actions schlägt fehl

- Prüfe die Logs unter Actions Tab
- Stelle sicher, dass `requirements.txt` korrekt ist
- Prüfe Python-Version in Workflow (aktuell 3.11)

### Artikel-Content ist leer

Die HTML-Struktur von Squarespace könnte sich geändert haben. Passe die Selektoren in `extract_blog_content()` an.

## 📄 Lizenz

MIT License - Nutze dieses Tool frei für deine eigenen Blogs.

## 🤝 Contributing

Verbesserungsvorschläge? Erstelle ein Issue oder Pull Request!

## 📞 Support

Bei Fragen oder Problemen öffne ein Issue in diesem Repository.

---

**Made with ❤️ for efficient knowledge management with Claude AI**
