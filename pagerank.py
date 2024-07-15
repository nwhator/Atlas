import sqlite3
import networkx as nx

# Connect to the SQLite Database
conn = sqlite3.connect('atlas.db')
cursor = conn.cursor()

# Retreive the URLs of all websites from the database
cursor.execute('SELECT url FROM pages')
urls = [row[0] for row in cursor.fetchall()]

# Create an empty directed graph using networkx
graph = nx.DiGraph()

# Add node to the graph
for url in urls:
    graph.add_node(url)

# Retrive the outgoing links of each website from the database and add the edges to the graph
for url in urls:
    cursor.execute('SELECT outgoing_links FROM pages WHERE url = ?', (url,))
    outgoing_links = cursor.fetchone()[0].split(',')
    
    for link in outgoing_links:
        if link.startswith('http'):
            graph.add_edge(url, link)
            
# Calculate the PageRank of each website
pagerank = nx.pagerank(graph)

# Store the pagerank scores in the database
for url in urls:
    cursor.execute("UPDATE pages SET pagerank = ? WHERE url = ?",
                   (pagerank[url], url))
    
# Commit the changes to the database
conn.commit()

# Close the database
conn.close()
