#!/usr/bin/env python3
"""
Artikel-Kombinierer für Claude AI
Kombiniert alle oder gefilterte Artikel in eine einzelne Datei
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def load_index(blog_dir):
    """Lade die Index-Datei"""
    index_path = Path(blog_dir) / "index.json"
    if not index_path.exists():
        print("❌ Keine index.json gefunden. Führe erst blog_crawler.py aus.")
        return None
    
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def combine_articles(blog_dir, output_file, filter_author=None, filter_from_date=None, 
                    filter_keyword=None, max_articles=None):
    """Kombiniere Artikel basierend auf Filtern"""
    
    blog_path = Path(blog_dir)
    index = load_index(blog_dir)
    
    if not index:
        return
    
    print(f"📚 Gefundene Artikel: {len(index['articles'])}")
    
    # Filter anwenden
    articles = index['articles']
    
    if filter_author:
        articles = [a for a in articles if filter_author.lower() in a['author'].lower()]
        print(f"   → Nach Autor '{filter_author}' gefiltert: {len(articles)} Artikel")
    
    if filter_from_date:
        # Vereinfachtes Datum-Filtering
        articles = [a for a in articles if a['date'] >= filter_from_date]
        print(f"   → Ab Datum '{filter_from_date}' gefiltert: {len(articles)} Artikel")
    
    if filter_keyword:
        filtered = []
        for article in articles:
            filepath = blog_path / article['filename']
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if filter_keyword.lower() in content:
                        filtered.append(article)
        articles = filtered
        print(f"   → Nach Keyword '{filter_keyword}' gefiltert: {len(articles)} Artikel")
    
    if max_articles and len(articles) > max_articles:
        articles = articles[:max_articles]
        print(f"   → Limitiert auf {max_articles} Artikel")
    
    if not articles:
        print("❌ Keine Artikel nach Filterung übrig!")
        return
    
    # Kombiniere Artikel
    print(f"\n📝 Kombiniere {len(articles)} Artikel...")
    
    combined = f"""# Blog-Archiv für Claude AI

Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Anzahl Artikel: {len(articles)}
Quelle: {index['base_url']}

---

"""
    
    for i, article in enumerate(articles, 1):
        filepath = blog_path / article['filename']
        
        if not filepath.exists():
            print(f"   ⚠️  Datei nicht gefunden: {article['filename']}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Entferne das Frontmatter für die kombinierte Version (optional)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        
        combined += f"\n\n{'='*80}\n"
        combined += f"ARTIKEL {i}/{len(articles)}\n"
        combined += f"{'='*80}\n\n"
        combined += content
        
        print(f"   [{i}/{len(articles)}] {article['title']}")
    
    # Speichere kombinierte Datei
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(combined)
    
    print(f"\n✅ Erfolgreich kombiniert!")
    print(f"💾 Gespeichert als: {output_path}")
    print(f"📊 Dateigröße: {output_path.stat().st_size / 1024:.1f} KB")
    
    # Warnungen zur Token-Größe
    estimated_tokens = len(combined.split()) * 1.3  # Grobe Schätzung
    print(f"⚠️  Geschätzte Tokens: ~{estimated_tokens:,.0f}")
    
    if estimated_tokens > 100000:
        print("   ⚠️  WARNUNG: Datei könnte zu groß für Claude's Kontext sein!")
        print("   💡 Tipp: Nutze Filter um die Artikelanzahl zu reduzieren")


def create_summary(blog_dir, output_file):
    """Erstelle eine Übersicht aller Artikel (nur Metadaten)"""
    
    index = load_index(blog_dir)
    if not index:
        return
    
    summary = f"""# Blog-Artikel Übersicht

Stand: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Gesamt: {len(index['articles'])} Artikel

## Alle Artikel

"""
    
    # Gruppiere nach Autor
    by_author = {}
    for article in index['articles']:
        author = article['author']
        if author not in by_author:
            by_author[author] = []
        by_author[author].append(article)
    
    for author, articles in sorted(by_author.items()):
        summary += f"\n### {author} ({len(articles)} Artikel)\n\n"
        for article in sorted(articles, key=lambda x: x['date'], reverse=True):
            summary += f"- **{article['title']}** ({article['date']})\n"
            summary += f"  - Datei: `{article['filename']}`\n"
            summary += f"  - URL: {article['url']}\n\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ Übersicht erstellt: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Kombiniere Blog-Artikel für Claude AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Alle Artikel kombinieren
  python combine_for_claude.py
  
  # Nur Artikel von einem Autor
  python combine_for_claude.py --author "Otis Benning"
  
  # Nur die neuesten 20 Artikel
  python combine_for_claude.py --max 20
  
  # Artikel mit bestimmtem Keyword
  python combine_for_claude.py --keyword "Geldwäsche"
  
  # Nur Metadaten-Übersicht erstellen
  python combine_for_claude.py --summary-only
        """
    )
    
    parser.add_argument(
        '--blog-dir',
        default='blog_content',
        help='Verzeichnis mit den gecrawlten Artikeln (default: blog_content)'
    )
    
    parser.add_argument(
        '--output',
        default='combined_for_claude.md',
        help='Output-Datei (default: combined_for_claude.md)'
    )
    
    parser.add_argument(
        '--author',
        help='Filtere nach Autor (Teil-Match möglich)'
    )
    
    parser.add_argument(
        '--from-date',
        help='Nur Artikel ab diesem Datum (Format: DD.MM.YY)'
    )
    
    parser.add_argument(
        '--keyword',
        help='Filtere nach Keyword im Content'
    )
    
    parser.add_argument(
        '--max',
        type=int,
        help='Maximale Anzahl an Artikeln'
    )
    
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Erstelle nur eine Übersicht (keine Volltexte)'
    )
    
    args = parser.parse_args()
    
    if args.summary_only:
        create_summary(args.blog_dir, args.output)
    else:
        combine_articles(
            args.blog_dir,
            args.output,
            filter_author=args.author,
            filter_from_date=args.from_date,
            filter_keyword=args.keyword,
            max_articles=args.max
        )


if __name__ == "__main__":
    main()
