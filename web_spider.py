import requests
from bs4 import BeautifulSoup
import sqlite3

def crawler(start_url, max_pages = 100):
    
    # Connect to SQLite database
    
    conn = sqlite3.connect('atlas.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                content TEXT,
                cleaned_content TEXT,
                title TEXT,
                outgoing_links TEXT,
                pagerank REAL
              )
              ''')
    conn.commit()

    # Initialize the URL frontier with the start URL
    
    url_frontier = [start_url]
    
    visited_pages = set()
    
    while url_frontier and len(visited_pages) < max_pages:

        # Get the next URL from the frontier
    
      url = url_frontier.pop(0)

        # Skip if the URL has already been visited 
        
      if url in visited_pages:
        continue

      print(f"Crawling {url}")
      response = requests.get(url)

        # Skip if the request was unsuccesful

      if response.status_code != 200:
        continue
  
      soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the page title
      
      if soup.find('title'):
        title = soup.find('title').string

        # Extract the outgoing links
        
      outgoing_links = []
      for link in soup.find_all('a'):
        href = link.get('href')
        if href:
          outgoing_links.append(href)

        # Insert page data into the database
      
      c.execute('INSERT OR IGNORE INTO pages (url, content, cleaned_content, title, outgoing_links) VALUES(?, ?, ?, ?, ?)', 
                (url, str(soup), soup.get_text(), title, ','.join(outgoing_links)))
                
      conn.commit()

        # Add new links to the frontier
      
      links = soup.find_all('a')

      for link in links:
          href = link.get("href")
          if href and 'http' in href and href not in visited_pages:
              url_frontier.append(href)

        # Mark the URL as visited
        
      visited_pages.add(url)

    # Close the database connection
    
    conn.close()
    print("Crawling Complete.")

# Seed URLs to start the crwaling process

seed_urls = ["https://www.bbc.co.uk/sport/football", "https://www.cnn.com"]
for url in seed_urls:
    crawler(url, 100)
