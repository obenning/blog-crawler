#!/usr/bin/env python3
"""
Kombiniere alle Blog-Artikel in ein großes Dokument für KI-Nutzung
"""

from pathlib import Path
from datetime import datetime

def combine_all_articles(blog_dir="blog_content", output_file="ALL_ARTICLES_COMBINED.md"):
    """
    Kombiniere alle Artikel in ein großes Markdown-Dokument
    """
    blog_path = Path(blog_dir)
    
    if not blog_path.exists():
        print(f"❌ Ordner {blog_dir} existiert nicht!")
        return False
    
    articles = []
    
    # Sammle alle Artikel
    for md_file in sorted(blog_path.glob("*.md")):
        # Überspringe das kombinierte Dokument selbst
        if md_file.name == output_file:
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Frontmatter für Metadaten
            metadata = {}
            body = content
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    body = parts[2].strip()
                    
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"\'')
            
            articles.append({
                'filename': md_file.name,
                'title': metadata.get('title', md_file.stem.replace('-', ' ').title()),
                'author': metadata.get('author', 'Unknown'),
                'date': metadata.get('date', ''),
                'url': metadata.get('url', ''),
                'body': body,
                'word_count': len(body.split())
            })
            
        except Exception as e:
            print(f"⚠️  Fehler bei {md_file.name}: {e}")
            continue
    
    if not articles:
        print("❌ Keine Artikel gefunden!")
        return False
    
    # Sortiere nach Datum (neueste zuerst)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Erstelle kombiniertes Dokument
    output = []
    output.append("# 📚 Kerberos Compliance Blog - Alle Artikel")
    output.append("")
    output.append(f"**Generiert:** {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    output.append(f"**Anzahl Artikel:** {len(articles)}")
    output.append(f"**Gesamtwortanzahl:** {sum(a['word_count'] for a in articles):,}")
    output.append("")
    output.append("---")
    output.append("")
    output.append("## 📋 Inhaltsverzeichnis")
    output.append("")
    
    # Inhaltsverzeichnis
    for i, article in enumerate(articles, 1):
        # Erstelle Anchor-Link
        anchor = article['title'].lower()
        anchor = ''.join(c if c.isalnum() or c.isspace() else '' for c in anchor)
        anchor = anchor.replace(' ', '-')
        output.append(f"{i}. [{article['title']}](#{anchor})")
    
    output.append("")
    output.append("---")
    output.append("")
    
    # Artikel-Inhalt
    for i, article in enumerate(articles, 1):
        output.append(f"## {i}. {article['title']}")
        output.append("")
        output.append(f"**Autor:** {article['author']}  ")
        output.append(f"**Datum:** {article['date']}  ")
        output.append(f"**Wortanzahl:** {article['word_count']:,}  ")
        if article['url']:
            output.append(f"**Original:** {article['url']}  ")
        output.append("")
        output.append("---")
        output.append("")
        output.append(article['body'])
        output.append("")
        output.append("---")
        output.append("")
    
    # Speichere kombiniertes Dokument
    output_path = blog_path / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    total_size = output_path.stat().st_size / (1024 * 1024)  # MB
    
    print(f"✅ Kombiniertes Dokument erstellt: {output_path}")
    print(f"   📊 {len(articles)} Artikel")
    print(f"   📝 {sum(a['word_count'] for a in articles):,} Wörter")
    print(f"   💾 {total_size:.2f} MB")
    print(f"\n🌐 KI-freundliche URL:")
    print(f"   https://raw.githubusercontent.com/obenning/blog-crawler/main/{blog_dir}/{output_file}")
    
    return True


if __name__ == "__main__":
    import sys
    
    blog_dir = sys.argv[1] if len(sys.argv) > 1 else "blog_content"
    
    print("=" * 60)
    print("📚 Kombiniere alle Artikel")
    print("=" * 60)
    print()
    
    success = combine_all_articles(blog_dir)
    
    if success:
        print("\n✨ Fertig! Du kannst jetzt:")
        print("   1. git add blog_content/ALL_ARTICLES_COMBINED.md")
        print("   2. git commit -m 'Add combined articles document'")
        print("   3. git push")
    else:
        print("\n❌ Fehler beim Kombinieren")
        sys.exit(1)
