#!/usr/bin/env python3
"""
Squarespace Blog Crawler
Crawelt alle Blog-Artikel und speichert sie strukturiert als Markdown-Dateien
"""

import requests
from bs4 import BeautifulSoup
import os
import json
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re
from pathlib import Path

class SquarespaceBlogCrawler:
    def __init__(self, base_url, output_dir="blog_content"):
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_page(self, url, retries=3):
        """Hole eine Seite mit Retry-Logik"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == retries - 1:
                    print(f"❌ Fehler beim Laden von {url}: {e}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def extract_blog_post_urls(self, soup):
        """Extrahiere alle Blog-Post-URLs aus der Übersichtsseite"""
        urls = []
        
        # Finde alle Blog-Post-Links in der Übersichtsseite
        for article in soup.find_all('article', class_='blog-item'):
            title_link = article.find('h1', class_='blog-title')
            if title_link:
                link = title_link.find('a')
                if link and link.get('href'):
                    full_url = urljoin(self.base_url, link['href'])
                    urls.append(full_url)
        
        return urls
    
    def get_next_page_url(self, soup):
        """Finde den Link zur nächsten Seite"""
        pagination = soup.find('nav', class_='blog-list-pagination')
        if pagination:
            older_link = pagination.find('div', class_='older')
            if older_link:
                link = older_link.find('a')
                if link and link.get('href'):
                    return urljoin(self.base_url, link['href'])
        return None
    
    def crawl_all_post_urls(self):
        """Crawle alle Seiten und sammle alle Blog-Post-URLs"""
        all_urls = []
        current_url = self.base_url
        page_count = 1
        
        while current_url:
            print(f"📄 Crawle Übersichtsseite {page_count}...")
            response = self.get_page(current_url)
            if not response:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrahiere URLs von dieser Seite
            urls = self.extract_blog_post_urls(soup)
            all_urls.extend(urls)
            print(f"   ✓ {len(urls)} Artikel gefunden")
            
            # Finde nächste Seite
            current_url = self.get_next_page_url(soup)
            page_count += 1
            
            # Kurze Pause zwischen Requests
            time.sleep(1)
        
        print(f"\n✅ Insgesamt {len(all_urls)} Blog-Artikel gefunden")
        return all_urls
    
    def extract_blog_content(self, soup, url):
        """Extrahiere den Inhalt eines einzelnen Blog-Posts - Verbesserte Version"""
        article_data = {
            'url': url,
            'title': '',
            'author': '',
            'date': '',
            'content': '',
            'excerpt': '',
            'crawled_at': datetime.now().isoformat()
        }
        
        # Titel - erweiterte Suche
        title_elem = None
        title_selectors = [
            soup.find('h1', class_='blog-title'),
            soup.find('h1', class_='entry-title'),
            soup.find('h1', class_='post-title'),
            soup.find('header', class_='entry-header'),
            soup.find('h1')
        ]
        
        for elem in title_selectors:
            if elem:
                title_elem = elem
                break
        
        if title_elem:
            # Wenn header, suche h1 darin
            if title_elem.name == 'header':
                h1 = title_elem.find('h1')
                title_elem = h1 if h1 else title_elem
            article_data['title'] = title_elem.get_text(strip=True)
        
        # Autor und Datum aus Meta-Section
        meta_section = soup.find('div', class_='blog-meta-section')
        if meta_section:
            author_elem = meta_section.find('span', class_='blog-author')
            if author_elem:
                article_data['author'] = author_elem.get_text(strip=True)
            
            date_elem = meta_section.find('time', class_='blog-date')
            if date_elem:
                article_data['date'] = date_elem.get_text(strip=True)
        
        # Excerpt
        excerpt_elem = soup.find('div', class_='blog-excerpt')
        if excerpt_elem:
            article_data['excerpt'] = excerpt_elem.get_text(strip=True)
        
        # Hauptinhalt - ROBUSTE STRATEGIE
        content = None
        
        # Strategie 1: Suche nach bekannten Content-Containern
        content_selectors = [
            soup.find('div', class_='blog-item-content'),
            soup.find('div', class_='entry-content'),
            soup.find('div', class_='post-content'),
            soup.find('div', class_='blog-content'),
            soup.find('article', class_='entry'),
            soup.find('article', class_='blog-item'),
        ]
        
        for selector in content_selectors:
            if selector:
                content = selector
                break
        
        # Strategie 2: Wenn nichts gefunden, suche nach article Tag
        if not content:
            article = soup.find('article')
            if article:
                content = article
        
        # Strategie 3: Suche nach dem größten Content-Block mit Text
        if not content or len(content.get_text(strip=True)) < 100:
            # Finde alle divs mit substantiellem Text
            all_divs = soup.find_all(['div', 'section', 'article'])
            best_div = None
            max_text_length = 0
            
            for div in all_divs:
                # Ignoriere Navigation, Header, Footer
                classes = div.get('class', [])
                if any(x in str(classes).lower() for x in ['nav', 'header', 'footer', 'sidebar', 'menu']):
                    continue
                
                text = div.get_text(strip=True)
                # Suche nach Div mit viel Text UND Paragraphen
                paragraphs = div.find_all('p', recursive=False) or div.find_all('p')
                if len(text) > max_text_length and len(paragraphs) > 0:
                    max_text_length = len(text)
                    best_div = div
            
            if best_div and max_text_length > 200:
                content = best_div
        
        # Strategie 4: Letzter Ausweg - suche nach main Tag oder body
        if not content or len(content.get_text(strip=True)) < 100:
            main = soup.find('main')
            if main:
                content = main
        
        if content:
            # Entferne Navigation, Sidebar, etc.
            for unwanted in content.find_all(['nav', 'aside', 'footer', 'header']):
                unwanted.decompose()
            
            # Entferne auch bekannte Squarespace-Elemente die nicht zum Content gehören
            for class_name in ['blog-meta-section', 'blog-title', 'blog-author', 
                              'blog-date', 'blog-list-pagination', 'blog-more-link']:
                for elem in content.find_all(class_=class_name):
                    elem.decompose()
            
            # Entferne Skripte und Styles
            for element in content.find_all(['script', 'style']):
                element.decompose()
            
            # Extrahiere Text und formatiere
            article_data['content'] = self.clean_content(content)
        
        return article_data
    
    def clean_content(self, content_element):
        """Bereinige und formatiere den Content mit Links - Verbesserte Version"""
        lines = []
        
        def extract_text_with_links(element):
            """Extrahiere Text aus einem Element und behalte Links"""
            if element.name is None:
                # Text node
                text = str(element).strip()
                return text if text else ''
            
            if element.name == 'a':
                # Link als Markdown
                text = element.get_text(strip=True)
                href = element.get('href')
                if href and text:
                    # Konvertiere zu absoluter URL
                    absolute_url = urljoin(self.base_url, href)
                    return f"[{text}]({absolute_url})"
                return text
            
            # Für andere Elemente: sammle Text von allen Kindern
            parts = []
            for child in element.children:
                part = extract_text_with_links(child)
                if part:
                    parts.append(part)
            
            return ' '.join(parts)
        
        def process_element(elem, depth=0):
            """Verarbeite ein Element rekursiv"""
            # Prüfe ob es ein echtes Element ist (kein Text-Knoten)
            if not elem or not hasattr(elem, 'name') or elem.name is None:
                return
            
            # Ignoriere bestimmte Elemente
            if elem.name in ['script', 'style', 'nav', 'aside']:
                return
            
            # Überschriften
            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = extract_text_with_links(elem)
                if text:
                    level = int(elem.name[1])
                    lines.append('\n' + '#' * level + ' ' + text + '\n')
            
            # Paragraphen
            elif elem.name == 'p':
                text = extract_text_with_links(elem)
                if text and len(text) > 1:  # Mindestens 1 Zeichen
                    lines.append(text + '\n')
            
            # Listen
            elif elem.name in ['ul', 'ol']:
                for li in elem.find_all('li', recursive=False):
                    text = extract_text_with_links(li)
                    if text:
                        lines.append('- ' + text)
            
            # Blockquotes
            elif elem.name == 'blockquote':
                text = extract_text_with_links(elem)
                if text:
                    lines.append('> ' + text + '\n')
            
            # Squarespace Content Blocks
            elif elem.name in ['div', 'section', 'article', 'main']:
                # Prüfe ob Squarespace Block
                elem_classes = elem.get('class', []) if hasattr(elem, 'get') else []
                is_sqs_block = 'sqs-block' in elem_classes
                
                if is_sqs_block:
                    # Verarbeite Kinder rekursiv
                    for child in elem.children:
                        if hasattr(child, 'name') and child.name:
                            process_element(child, depth + 1)
                else:
                    # Container-Elemente: Prüfe direkten Content
                    direct_children = [c for c in elem.children if hasattr(c, 'name') and c.name]
                    
                    # Wenn nur Container-Elemente als Kinder, dann rekursiv
                    if direct_children and all(c.name in ['div', 'section', 'article'] for c in direct_children):
                        for child in elem.children:
                            if hasattr(child, 'name') and child.name:
                                process_element(child, depth + 1)
                    else:
                        # Verarbeite alle Kinder
                        for child in elem.children:
                            if hasattr(child, 'name') and child.name:
                                process_element(child, depth + 1)
        
        # Starte Verarbeitung
        process_element(content_element)
        
        # Nachbearbeitung: Entferne übermäßige Leerzeilen
        result = '\n'.join(lines)
        
        # Reduziere mehrfache Leerzeilen auf maximal 2
        while '\n\n\n' in result:
            result = result.replace('\n\n\n', '\n\n')
        
        return result.strip()
    
    def sanitize_filename(self, title, url):
        """Erstelle einen sicheren Dateinamen"""
        # Versuche aus der URL einen Namen zu extrahieren
        path = urlparse(url).path
        slug = path.split('/')[-1]
        
        if not slug or slug == '':
            # Fallback: Nutze den Titel
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[-\s]+', '-', slug)
        
        return slug[:100] + '.md'  # Begrenze Länge
    
    def save_article(self, article_data):
        """Speichere einen Artikel als Markdown-Datei"""
        filename = self.sanitize_filename(article_data['title'], article_data['url'])
        filepath = self.output_dir / filename
        
        # Erstelle Markdown mit Frontmatter
        markdown = f"""---
title: "{article_data['title']}"
author: "{article_data['author']}"
date: "{article_data['date']}"
url: "{article_data['url']}"
excerpt: "{article_data['excerpt']}"
crawled_at: "{article_data['crawled_at']}"
---

# {article_data['title']}

**Autor:** {article_data['author']}  
**Datum:** {article_data['date']}  
**URL:** {article_data['url']}

---

{article_data['content']}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        return filename
    
    def crawl_article(self, url):
        """Crawle einen einzelnen Artikel"""
        response = self.get_page(url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        article_data = self.extract_blog_content(soup, url)
        
        if article_data['title']:
            filename = self.save_article(article_data)
            return filename
        
        return None
    
    def crawl_all(self):
        """Hauptfunktion: Crawle alle Blog-Posts"""
        print("🚀 Starte Blog-Crawler...")
        print(f"📍 Base URL: {self.base_url}")
        print(f"💾 Output: {self.output_dir}")
        print()
        
        # Sammle alle URLs
        all_urls = self.crawl_all_post_urls()
        
        if not all_urls:
            print("❌ Keine Blog-Posts gefunden!")
            return
        
        print(f"\n📥 Crawle {len(all_urls)} Artikel...\n")
        
        # Crawle jeden Artikel
        successful = 0
        failed = 0
        
        for i, url in enumerate(all_urls, 1):
            print(f"[{i}/{len(all_urls)}] Crawle: {url}")
            filename = self.crawl_article(url)
            
            if filename:
                print(f"   ✓ Gespeichert als: {filename}")
                successful += 1
            else:
                print(f"   ✗ Fehler beim Crawlen")
                failed += 1
            
            # Pause zwischen Requests
            time.sleep(1)
        
        # Erstelle Index-Datei
        self.create_index(all_urls, successful, failed)
        
        print(f"\n{'='*60}")
        print(f"✅ Crawling abgeschlossen!")
        print(f"   Erfolgreich: {successful}")
        print(f"   Fehlgeschlagen: {failed}")
        print(f"   Total: {len(all_urls)}")
        print(f"{'='*60}")
    
    def create_index(self, urls, successful, failed):
        """Erstelle eine Index-Datei mit Metadaten"""
        index_data = {
            'crawled_at': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_articles': len(urls),
            'successful': successful,
            'failed': failed,
            'articles': []
        }
        
        # Lese alle gespeicherten Artikel
        for md_file in self.output_dir.glob('*.md'):
            if md_file.name == 'README.md':
                continue
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extrahiere Frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    data = {}
                    for line in frontmatter.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            data[key.strip()] = value.strip().strip('"')
                    
                    index_data['articles'].append({
                        'filename': md_file.name,
                        'title': data.get('title', ''),
                        'author': data.get('author', ''),
                        'date': data.get('date', ''),
                        'url': data.get('url', '')
                    })
        
        # Speichere Index als JSON
        with open(self.output_dir / 'index.json', 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        
        # Erstelle auch ein README
        readme = f"""# Blog Content Archive

Automatisch gecrawlt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Statistik:**
- Gesamt Artikel: {len(urls)}
- Erfolgreich gecrawlt: {successful}
- Fehlgeschlagen: {failed}

**Quelle:** {self.base_url}

## Artikel

"""
        
        for article in sorted(index_data['articles'], key=lambda x: x['date'], reverse=True):
            readme += f"- [{article['title']}]({article['filename']}) - {article['author']} ({article['date']})\n"
        
        with open(self.output_dir / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme)
        
        print(f"\n📋 Index erstellt: index.json und README.md")


def main():
    # Konfiguration
    BASE_URL = "https://www.kerberos-compliance.com/wissen/blog"  # Anpassen!
    OUTPUT_DIR = "blog_content"
    
    # Crawler initialisieren und starten
    crawler = SquarespaceBlogCrawler(BASE_URL, OUTPUT_DIR)
    crawler.crawl_all()


if __name__ == "__main__":
    main()
