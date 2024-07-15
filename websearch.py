from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__, template_folder='./static')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/websearch', methods = ['GET', 'POST'])
def search():
    # Get query from the request
    query = request.form['query']
    
    if query == "":
        render_template('index.html')
        
    # Connect to the SQLite database
    conn = sqlite3.connect('atlas.db')
    cursor = conn.cursor()
    
    # Search for websites that match the query in their cleaned_content
    cursor.execute("SELECT url, title FROM pages WHERE cleaned_content\
        LIKE ? ORDER BY pagerank DESC", ('%' + query + '%',))
    urls = cursor.fetchall()
    
    # Close connection
    conn.close()
        
    # Render the URLs that match the query
    return render_template('results.html', urls=urls, query = query)


if __name__ == "__main__":
    app.run(debug=True)
