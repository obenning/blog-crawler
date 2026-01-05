# 🚀 Quick Start Guide

## In 5 Minuten zu deinem Blog-Archiv

### Schritt 1: Repository Setup (2 Min)

```bash
# Erstelle neues GitHub Repository auf github.com
# Name: blog-crawler (oder dein Wunschname)
# Visibility: Public oder Private (deine Wahl)

# Klone dieses Setup
git clone https://github.com/DEIN-USERNAME/blog-crawler.git
cd blog-crawler
```

### Schritt 2: URL anpassen (30 Sek)

Öffne `blog_crawler.py` und ändere Zeile 270:

```python
BASE_URL = "https://www.kerberos-compliance.com/wissen/blog"  
# ↓ Ändere zu deiner URL:
BASE_URL = "https://DEINE-SEITE.com/blog"
```

### Schritt 3: Ersten Test (1 Min)

```bash
# Dependencies installieren
pip install -r requirements.txt

# Crawler ausführen
python blog_crawler.py
```

✅ Du findest jetzt alle Artikel in `blog_content/`!

### Schritt 4: Zu GitHub pushen (1 Min)

```bash
git add .
git commit -m "Initial setup mit meiner Blog-URL"
git push
```

### Schritt 5: Automatisierung aktivieren (30 Sek)

Der Crawler läuft ab jetzt automatisch täglich um 2 Uhr!

✅ **Fertig!** Du kannst jetzt:

- Die Dateien aus `blog_content/` nutzen
- Über GitHub Actions den Status überwachen
- Artikel kombinieren mit `python combine_for_claude.py`

## 💡 Sofort nutzbar

### Für Claude vorbereiten

```bash
# Alle Artikel in eine Datei
python combine_for_claude.py

# Nur von einem Autor
python combine_for_claude.py --author "Dein Name"

# Nur die neuesten 10 Artikel
python combine_for_claude.py --max 10
```

### An Claude hochladen

1. Öffne Claude
2. Upload `combined_for_claude.md`
3. Stelle deine Frage:

```
Basierend auf den hochgeladenen Blog-Artikeln: 
Was sind die wichtigsten Themen zum Thema [DEIN THEMA]?
```

## 🎯 Nächste Schritte

1. **Automatisierung testen:**
   - Gehe zu deinem GitHub Repository
   - Klicke auf "Actions"
   - Klicke auf "Run workflow" → "Run workflow"
   
2. **Zeitplan anpassen:**
   - Bearbeite `.github/workflows/crawl-blog.yml`
   - Ändere die Cron-Zeile nach deinen Wünschen

3. **Filter nutzen:**
   - Nutze `combine_for_claude.py` mit verschiedenen Filtern
   - Erstelle mehrere kombinierte Dateien für verschiedene Themen

## ❓ Probleme?

**"No blog posts found"**
→ Überprüfe die BASE_URL in `blog_crawler.py`

**GitHub Actions schlägt fehl**
→ Schaue dir die Logs unter Actions → Latest Run an

**Artikel-Content ist leer**
→ Die HTML-Struktur könnte anders sein. Öffne ein Issue!

## 📚 Mehr Infos

- Ausführliche Anleitung: `README.md`
- Konfiguration: `config.ini`
- Code-Dokumentation: Im Quellcode

---

**Happy Crawling! 🎉**
