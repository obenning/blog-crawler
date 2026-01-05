# 🤖 KI-freundliche Blog-Suche - Setup-Anleitung

## 🎯 Ziel

Andere Personen können die Blog-Artikel einfach für ihre KIs (Claude, ChatGPT, etc.) nutzen - ohne GitHub API, nur mit `raw.githubusercontent.com` URLs.

## 📋 Was wird erstellt?

1. **articles_index.json** - JSON-Datei mit allen Artikel-Metadaten
2. **search_ai_friendly.html** - Such-Seite die raw.githubusercontent.com nutzt
3. **Automatische Updates** - GitHub Actions generiert Index automatisch

## 🚀 Setup (einmalig)

### Schritt 1: Dateien ins Repository kopieren

```powershell
cd C:\Users\BenningOtis\Downloads\blog-crawler-github

# Kopiere die neuen Dateien
Copy-Item "C:\Users\BenningOtis\Downloads\generate_index.py" -Destination .
Copy-Item "C:\Users\BenningOtis\Downloads\search_ai_friendly.html" -Destination .
```

### Schritt 2: JSON-Index generieren

```powershell
python generate_index.py
```

**Output:**
```
✅ Index generiert: blog_content\articles_index.json
   📊 116 Artikel
   📅 Generiert: 2026-01-05T...
```

### Schritt 3: GitHub Actions erweitern

Bearbeite `.github/workflows/crawl-blog.yml` und füge am Ende der `steps` hinzu:

```yaml
      - name: Generate KI-friendly index
        run: |
          python generate_index.py
        
      - name: Commit and push if changed
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add blog_content/*.json
          git diff --quiet && git diff --staged --quiet || (git commit -m "🤖 Auto-update: articles index" && git push)
```

### Schritt 4: Dateien committen

```powershell
git add generate_index.py
git add search_ai_friendly.html
git add blog_content/articles_index.json
git add .github/workflows/crawl-blog.yml

git commit -m "Add KI-friendly blog search interface"
git push
```

### Schritt 5: GitHub Pages aktivieren

1. Gehe zu: https://github.com/obenning/blog-crawler/settings/pages
2. **Source:** main branch
3. **Folder:** / (root)
4. Speichern

Kopiere `search_ai_friendly.html` auch als `index.html`:

```powershell
Copy-Item search_ai_friendly.html index.html
git add index.html
git commit -m "Add index page for GitHub Pages"
git push
```

Warte 2-3 Minuten, dann verfügbar unter:
**https://obenning.github.io/blog-crawler/**

## ✅ Fertig! Jetzt können andere nutzen:

### Option 1: Direkte Such-Seite

**Link teilen:**
```
https://obenning.github.io/blog-crawler/
```

**Was können Leute machen:**
1. Artikel suchen
2. "Raw-Link für KI" Button klicken
3. URL kopieren
4. In ihre KI einfügen

**Beispiel für Claude:**
```
Bitte analysiere diesen Artikel:
https://raw.githubusercontent.com/obenning/blog-crawler/main/blog_content/kampf-gegen-geldwsche-goldesel-auf-dem-weg-zum-goldstandard.md
```

### Option 2: JSON-Index direkt nutzen

**Für fortgeschrittene KI-Nutzer:**

```
Bitte lade diese Artikel-Übersicht:
https://raw.githubusercontent.com/obenning/blog-crawler/main/blog_content/articles_index.json

Zeige mir alle Artikel zum Thema "BaFin"
```

Claude kann dann die JSON-Datei laden und durchsuchen!

### Option 3: Für Entwickler

**Repository klonen:**
```bash
git clone https://github.com/obenning/blog-crawler.git
cd blog-crawler
```

**Alle Artikel verfügbar in:** `blog_content/*.md`

## 📧 Email-Template für Kollegen

```
Betreff: 🤖 Blog-Archiv jetzt KI-freundlich verfügbar!

Hallo,

unser Blog-Archiv ist jetzt optimal für KI-Nutzung aufbereitet.

🔍 Interaktive Suche:
https://obenning.github.io/blog-crawler/

So nutzt du es mit Claude/ChatGPT:

1. Öffne die Such-Seite
2. Suche nach deinem Thema (z.B. "BaFin Prüfung")
3. Klicke auf "🤖 Raw-Link für KI"
4. Kopiere den Link
5. Füge in deine KI ein:
   
   "Bitte analysiere diesen Artikel: [LINK]"

Beispiel-Link:
https://raw.githubusercontent.com/obenning/blog-crawler/main/blog_content/kampf-gegen-geldwsche-goldesel-auf-dem-weg-zum-goldstandard.md

✨ NEU: Das Archiv updated sich täglich automatisch!

Viel Erfolg mit den KI-gestützten Recherchen!

Beste Grüße
```

## 🔄 Automatische Updates

**GitHub Actions läuft täglich:**
1. Crawlt neue Artikel (2:00 UTC / 3:00 deutsche Zeit)
2. Generiert automatisch neuen JSON-Index
3. Pushed beides ins Repository

**Manueller Trigger:**
1. Gehe zu: https://github.com/obenning/blog-crawler/actions
2. Wähle "Crawl Kerberos Compliance Blog"
3. Klicke "Run workflow"

## 🎨 Anpassungen

### Logo/Branding hinzufügen

Bearbeite `search_ai_friendly.html`, Zeile ~60:

```html
<div class="header">
    <img src="https://example.com/logo.png" alt="Logo" style="height: 40px; margin-bottom: 1rem;">
    <h1>🤖 Kerberos Compliance Blog</h1>
    ...
</div>
```

### Farben ändern

Bearbeite CSS-Variablen in `search_ai_friendly.html`, Zeile ~20:

```css
.header {
    background: linear-gradient(135deg, #YOUR-COLOR-1 0%, #YOUR-COLOR-2 100%);
}
```

### Domain-Namen (optional)

Statt `obenning.github.io/blog-crawler` kannst du eine Custom Domain nutzen:

1. GitHub Settings → Pages → Custom domain
2. Trage Domain ein (z.B. `blog.kerberos-compliance.com`)
3. DNS-Einstellungen bei deinem Provider anpassen

## 🐛 Troubleshooting

### "Keine Artikel gefunden"

**Problem:** JSON-Index nicht verfügbar

**Lösung:**
```powershell
python generate_index.py
git add blog_content/articles_index.json
git commit -m "Add missing index"
git push
```

### "404 Not Found" bei raw.githubusercontent.com

**Problem:** Datei nicht im Repository

**Lösung:** Prüfe auf GitHub ob Datei existiert:
https://github.com/obenning/blog-crawler/blob/main/blog_content/articles_index.json

### GitHub Pages zeigt alte Version

**Lösung:** 
1. Warte 5-10 Minuten (GitHub Pages cached)
2. Erzwinge Neuaufbau: Settings → Pages → Speichern (erneut)

## 📊 Statistiken

Die Such-Seite zeigt automatisch:
- Anzahl der Artikel
- Generierungs-Datum des Index
- Filter nach Top-5-Autoren
- Wort-Anzahl pro Artikel

## 🚀 Erweiterte Features (optional)

### CSV-Export hinzufügen

Bearbeite `search_ai_friendly.html`, füge Button hinzu:

```html
<button onclick="exportCSV()">📥 Als CSV exportieren</button>

<script>
function exportCSV() {
    const csv = [
        ['Titel', 'Autor', 'Datum', 'URL', 'Raw-URL'],
        ...filteredArticles.map(a => [
            a.title, a.author, a.date, a.url, a.raw_url
        ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'blog-artikel.csv';
    a.click();
}
</script>
```

### Kategorien/Tags hinzufügen

1. Erweitere Frontmatter in Artikeln:
   ```yaml
   tags: ["BaFin", "Geldwäsche", "Prüfung"]
   ```

2. Erweitere `generate_index.py`:
   ```python
   'tags': metadata.get('tags', '').split(',')
   ```

3. Füge Tag-Filter zur Such-Seite hinzu

## 💡 Use Cases

### Schnelle Kundenanfrage

1. Kunde fragt: "Was schreibt ihr über BaFin-Prüfungen?"
2. Such-Seite öffnen → "BaFin Prüfung" suchen
3. Relevante Artikel-Links an KI geben
4. KI erstellt Zusammenfassung
5. An Kunde weiterleiten

### Interne Recherche

1. Kollege braucht Infos zu "EU-AML"
2. Such-Seite teilen
3. Kollege sucht selbst
4. Nutzt Raw-Links in eigener KI

### Sales-Meeting

1. Teile Bildschirm mit Such-Seite
2. Live-Demo der Suche
3. Zeige wie einfach KI-Integration ist
4. Raw-Link-Feature demonstrieren

## 📞 Support

Bei Fragen:
- GitHub Issues: https://github.com/obenning/blog-crawler/issues
- Email: [deine-email]

## 🎉 Erfolg!

Dein Blog ist jetzt:
- ✅ KI-freundlich zugänglich
- ✅ Durchsuchbar mit Preview
- ✅ Automatisch aktualisiert
- ✅ Für Kollegen nutzbar
- ✅ SharePoint-integrierbar (via iframe)

**Hauptlinks:**
- 🔍 Suche: https://obenning.github.io/blog-crawler/
- 📄 JSON: https://raw.githubusercontent.com/obenning/blog-crawler/main/blog_content/articles_index.json
- 💻 Repo: https://github.com/obenning/blog-crawler
