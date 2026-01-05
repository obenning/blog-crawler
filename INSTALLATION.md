# 📦 Installation & Setup - Vollständige Anleitung

## Übersicht

Dieses Setup erstellt ein automatisches Blog-Archiv-System, das:
1. ✅ Täglich alle deine Blog-Artikel crawlt
2. ✅ Sie als strukturierte Markdown-Dateien speichert
3. ✅ Automatisch auf GitHub aktualisiert
4. ✅ Für Claude AI optimiert bereitstellt

**Zeitaufwand:** 10-15 Minuten

---

## 🎯 Was du brauchst

- [ ] GitHub Account (kostenlos: github.com)
- [ ] Python 3.11+ installiert (python.org)
- [ ] Git installiert (git-scm.com)
- [ ] Deine Blog-URL

---

## 📝 Schritt-für-Schritt Anleitung

### 1️⃣ GitHub Repository erstellen

**1.1 Auf GitHub einloggen**
- Gehe zu: https://github.com
- Logge dich ein (oder erstelle einen Account)

**1.2 Neues Repository erstellen**
- Klicke oben rechts auf das **+** Symbol
- Wähle **"New repository"**
- Gib einen Namen ein: `blog-crawler`
- Wähle **Public** (empfohlen) oder **Private**
- ✅ Aktiviere: **"Add a README file"**
- Klicke **"Create repository"**

**1.3 Repository klonen**

Öffne dein Terminal/Kommandozeile:

```bash
# Ersetze DEIN-USERNAME mit deinem GitHub-Username
git clone https://github.com/DEIN-USERNAME/blog-crawler.git
cd blog-crawler
```

---

### 2️⃣ Projektdateien hinzufügen

**2.1 Lade alle Dateien aus dem outputs-Ordner herunter**

Die benötigten Dateien sind:
- `blog_crawler.py` - Haupt-Crawler
- `combine_for_claude.py` - Artikel-Kombinierer
- `requirements.txt` - Python Dependencies
- `config.ini` - Konfiguration
- `.gitignore` - Git Ignorier-Regeln
- `README.md` - Dokumentation
- `QUICKSTART.md` - Schnellanleitung
- `.github/workflows/crawl-blog.yml` - Automatisierung

**2.2 Kopiere alle Dateien in dein Repository-Verzeichnis**

```bash
# Stelle sicher, dass du im blog-crawler Ordner bist
pwd  # Sollte .../blog-crawler anzeigen

# Kopiere alle heruntergeladenen Dateien hierhin
# (oder ziehe sie per Drag & Drop in den Ordner)
```

---

### 3️⃣ Blog-URL konfigurieren

**3.1 Öffne `blog_crawler.py` in einem Texteditor**

Gehe zur Zeile ~270 (am Ende der Datei):

```python
def main():
    # Konfiguration
    BASE_URL = "https://www.kerberos-compliance.com/wissen/blog"  # ← HIER ÄNDERN!
    OUTPUT_DIR = "blog_content"
```

**3.2 Ersetze die URL durch deine Blog-URL**

```python
    BASE_URL = "https://DEINE-SEITE.com/dein-blog"  # Deine URL hier
```

💡 **Wichtig:** Die URL sollte auf die Blog-Übersichtsseite zeigen!

**3.3 Speichere die Datei**

---

### 4️⃣ Lokaler Test (empfohlen)

Bevor du alles automatisierst, teste lokal:

**4.1 Python Dependencies installieren**

```bash
# Stelle sicher, dass Python 3.11+ installiert ist
python --version  # Sollte 3.11 oder höher sein

# Installiere Requirements
pip install -r requirements.txt
```

**4.2 Crawler ausführen**

```bash
python blog_crawler.py
```

Das dauert je nach Anzahl der Artikel einige Minuten.

**4.3 Ergebnis prüfen**

```bash
# Schaue in den blog_content Ordner
ls blog_content/

# Sollte zeigen:
# - *.md Dateien (deine Artikel)
# - index.json
# - README.md
```

✅ **Wenn du Artikel siehst, funktioniert alles!**

---

### 5️⃣ Zu GitHub pushen

**5.1 Git konfigurieren (nur beim ersten Mal)**

```bash
git config --global user.name "Dein Name"
git config --global user.email "deine@email.com"
```

**5.2 Alle Dateien hinzufügen**

```bash
# Füge alle Dateien hinzu
git add .

# Erstelle einen Commit
git commit -m "Initial setup: Blog-Crawler konfiguriert"

# Pushe zu GitHub
git push
```

**5.3 Auf GitHub prüfen**

- Gehe zu deinem Repository auf GitHub
- Du solltest jetzt alle Dateien sehen
- Der `blog_content/` Ordner enthält deine Artikel

---

### 6️⃣ GitHub Actions aktivieren

**Das war's - es läuft automatisch!** 🎉

Der Crawler wird ab jetzt automatisch ausgeführt:
- **Täglich um 2:00 Uhr UTC**
- **Bei jedem Push** (zum Testen)
- **Manuell** (siehe unten)

**6.1 Status überprüfen**

1. Gehe zu deinem Repository auf GitHub
2. Klicke auf den **"Actions"** Tab
3. Du siehst die Workflow-Runs

**6.2 Manuell ausführen**

1. Gehe zu **Actions** Tab
2. Klicke auf **"Crawl Blog Content"**
3. Klicke **"Run workflow"** → **"Run workflow"**
4. Warte ca. 2-5 Minuten
5. Prüfe die Ergebnisse

---

### 7️⃣ Für Claude vorbereiten

**Option A: Einzelne Artikel nutzen**

```bash
# Gehe zum blog_content Ordner
cd blog_content

# Artikel ansehen
ls *.md
```

Lade die benötigten `.md` Dateien zu Claude hoch.

**Option B: Alle Artikel kombinieren**

```bash
# Zurück zum Hauptverzeichnis
cd ..

# Alle Artikel kombinieren
python combine_for_claude.py

# Datei: combined_for_claude.md ist erstellt
```

**Option C: Gefiltert kombinieren**

```bash
# Nur Artikel von einem Autor
python combine_for_claude.py --author "Otis Benning"

# Nur die neuesten 20 Artikel
python combine_for_claude.py --max 20

# Nur Artikel mit Keyword "Compliance"
python combine_for_claude.py --keyword "Compliance"

# Nur Übersicht (keine Volltexte)
python combine_for_claude.py --summary-only
```

---

## ⚙️ Erweiterte Konfiguration

### Zeitplan anpassen

Bearbeite `.github/workflows/crawl-blog.yml`:

```yaml
schedule:
  # Aktuelle Einstellung: Täglich um 2:00 Uhr
  - cron: '0 2 * * *'
  
  # Beispiele:
  # Jede Stunde:
  # - cron: '0 * * * *'
  
  # Zweimal täglich (6:00 und 18:00):
  # - cron: '0 6,18 * * *'
  
  # Jeden Montag um 8:00:
  # - cron: '0 8 * * 1'
  
  # Werktags um 9:00:
  # - cron: '0 9 * * 1-5'
```

Speichern, committen und pushen:

```bash
git add .github/workflows/crawl-blog.yml
git commit -m "Zeitplan angepasst"
git push
```

---

## 🔧 Troubleshooting

### Problem: "No blog posts found"

**Lösung 1:** Überprüfe die URL
```python
# In blog_crawler.py
BASE_URL = "https://..."  # Stimmt die URL?
```

**Lösung 2:** Teste im Browser
- Öffne deine Blog-URL im Browser
- Sollten dort Artikel zu sehen sein?

**Lösung 3:** HTML-Struktur prüfen
- Squarespace könnte die Struktur geändert haben
- Kontaktiere mich für Anpassungen

### Problem: GitHub Actions schlägt fehl

**Lösung 1:** Logs ansehen
1. Gehe zu Actions Tab
2. Klicke auf den fehlgeschlagenen Run
3. Klicke auf den Job
4. Lies die Fehlermeldung

**Lösung 2:** Lokal testen
```bash
python blog_crawler.py
```
Funktioniert es lokal?

**Lösung 3:** Python-Version
- GitHub Actions nutzt Python 3.11
- Teste lokal mit gleicher Version

### Problem: Artikel-Content ist leer

**Ursache:** HTML-Struktur von Squarespace hat sich geändert

**Lösung:** Selektoren anpassen in `blog_crawler.py`:

```python
def extract_blog_content(self, soup, url):
    # Zeile ~150
    content_selectors = [
        {'class': 'blog-item-content'},
        {'class': 'entry-content'},
        # Füge weitere Selektoren hinzu:
        {'class': 'NEUE-KLASSE'},
    ]
```

### Problem: "Permission denied" bei git push

**Lösung 1:** SSH Key einrichten
```bash
# Generiere SSH Key
ssh-keygen -t ed25519 -C "deine@email.com"

# Füge zu GitHub hinzu:
# Settings → SSH Keys → New SSH Key
```

**Lösung 2:** HTTPS mit Token nutzen
- Erstelle Personal Access Token auf GitHub
- Nutze diesen als Passwort beim Push

---

## 📊 Monitoring & Wartung

### Regelmäßige Checks

**Wöchentlich:**
- Gehe zu Actions Tab
- Prüfe ob Workflows erfolgreich laufen
- Schaue in `blog_content/index.json` für Statistiken

**Monatlich:**
- Prüfe ob neue Artikel erfasst wurden
- Aktualisiere ggf. Python Dependencies:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

### Benachrichtigungen einrichten

**Email-Benachrichtigungen:**
1. GitHub Settings → Notifications
2. Aktiviere "Actions" Benachrichtigungen

---

## 🎓 Best Practices

### 1. Regelmäßig aktualisieren

```bash
# Ziehe Updates vom Repository
git pull

# Führe Crawler aus
python blog_crawler.py

# Pushe Änderungen
git add .
git commit -m "Update: Neue Artikel"
git push
```

### 2. Backups erstellen

```bash
# Erstelle Backup des blog_content Ordners
cp -r blog_content blog_content_backup_$(date +%Y%m%d)
```

### 3. Filter für Claude nutzen

Zu viele Artikel? Nutze Filter:

```bash
# Nur relevante Themen
python combine_for_claude.py --keyword "Dein Thema"

# Nur neueste Artikel
python combine_for_claude.py --max 30
```

---

## 📚 Nächste Schritte

1. ✅ **Setup abgeschlossen!**
2. 🔄 **Warte auf ersten automatischen Crawl** (morgen 2:00 Uhr)
3. 📖 **Nutze Artikel mit Claude:**
   - Upload `combined_for_claude.md`
   - Stelle Fragen basierend auf deinem Blog-Archiv
4. 🎯 **Experimentiere mit Filtern:**
   - Verschiedene Author-Filter
   - Keyword-Suchen
   - Zeitbasierte Filter

---

## 💡 Tipps für Claude

### Gute Prompts

```
Ich habe dir alle meine Blog-Artikel zur Verfügung gestellt.
Bitte analysiere die wichtigsten Trends zum Thema [THEMA].
```

```
Basierend auf den hochgeladenen Artikeln: 
Erstelle eine Zusammenfassung der Entwicklung von [THEMA] 
über die letzten 12 Monate.
```

```
Finde alle Artikel, die sich mit [THEMA] beschäftigen und 
erstelle eine strukturierte Übersicht der Kernaussagen.
```

### Token-Management

Claude hat ein Kontext-Limit. Wenn `combined_for_claude.md` zu groß ist:

1. **Nutze Filter:**
   ```bash
   python combine_for_claude.py --max 20
   ```

2. **Erstelle thematische Sammlungen:**
   ```bash
   python combine_for_claude.py --keyword "Compliance" --output compliance_artikel.md
   python combine_for_claude.py --keyword "Audit" --output audit_artikel.md
   ```

3. **Nutze nur Übersicht:**
   ```bash
   python combine_for_claude.py --summary-only
   ```
   Dann gezielt einzelne Artikel uploaden.

---

## 🆘 Support

**Probleme? Fragen?**

1. Prüfe die Logs in GitHub Actions
2. Teste lokal mit `python blog_crawler.py`
3. Schaue in `README.md` für Details
4. Kontaktiere Claude für Hilfe 😊

---

**Viel Erfolg mit deinem automatischen Blog-Archiv! 🚀**
