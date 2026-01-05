#!/usr/bin/env python3
"""
Generiere articles_index.json für KI-freundlichen Zugriff
Dieses Script erstellt eine JSON-Datei mit allen Artikel-Metadaten
"""

import json
from datetime import datetime
from pathlib import Path

def generate_articles_index(blog_dir="blog_content", output_file="articles_index.json"):
    """
    Generiere eine JSON-Index-Datei mit allen Artikel-Metadaten
    für KI-freundlichen Zugriff via raw.githubusercontent.com
    """
    articles = []
    blog_path = Path(blog_dir)
    
    if not blog_path.exists():
        print(f"❌ Ordner {blog_dir} existiert nicht!")
        return False
    
    print(f"📁 Durchsuche {blog_dir}...")
    
    # Durchsuche alle Markdown-Dateien
    md_files = sorted(blog_path.glob("*.md"))
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    body = parts[2].strip()
                    
                    # Extrahiere Metadaten
                    metadata = {}
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip().strip('"\'')
                    
                    # Erstelle Excerpt (erste 200 Zeichen des Body)
                    excerpt = metadata.get('excerpt', '')
                    if not excerpt and body:
                        # Entferne führende Leerzeichen/Newlines
                        clean_body = body.lstrip()
                        if len(clean_body) > 200:
                            excerpt = clean_body[:200] + '...'
                        else:
                            excerpt = clean_body
                    
                    # Erstelle Artikel-Eintrag
                    article = {
                        'filename': md_file.name,
                        'title': metadata.get('title', md_file.stem.replace('-', ' ').title()),
                        'author': metadata.get('author', 'Unknown'),
                        'date': metadata.get('date', ''),
                        'url': metadata.get('url', ''),
                        'excerpt': excerpt,
                        'raw_url': f'https://raw.githubusercontent.com/obenning/blog-crawler/main/{blog_dir}/{md_file.name}',
                        'word_count': len(body.split())
                    }
                    
                    articles.append(article)
                    print(f"  ✓ {md_file.name}")
        
        except Exception as e:
            print(f"  ⚠️  Fehler bei {md_file.name}: {e}")
            continue
    
    if not articles:
        print("❌ Keine Artikel gefunden!")
        return False
    
    # Sortiere nach Datum (neueste zuerst)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Speichere als JSON
    index_data = {
        'generated': datetime.now().isoformat(),
        'total_articles': len(articles),
        'articles': articles
    }
    
    index_path = blog_path / output_file
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Index generiert: {index_path}")
    print(f"   📊 {len(articles)} Artikel")
    print(f"   📅 Generiert: {index_data['generated']}")
    print(f"\n🌐 KI-freundliche URL:")
    print(f"   https://raw.githubusercontent.com/obenning/blog-crawler/main/{blog_dir}/{output_file}")
    
    return True


if __name__ == "__main__":
    import sys
    
    blog_dir = sys.argv[1] if len(sys.argv) > 1 else "blog_content"
    
    print("=" * 60)
    print("🤖 Generiere KI-freundlichen Artikel-Index")
    print("=" * 60)
    print()
    
    success = generate_articles_index(blog_dir)
    
    if success:
        print("\n✨ Fertig! Du kannst jetzt:")
        print("   1. git add blog_content/articles_index.json")
        print("   2. git commit -m 'Add KI-friendly article index'")
        print("   3. git push")
        print("\n📚 Dann ist der Index verfügbar unter:")
        print("   https://raw.githubusercontent.com/obenning/blog-crawler/main/blog_content/articles_index.json")
    else:
        print("\n❌ Fehler beim Generieren des Index")
        sys.exit(1)
