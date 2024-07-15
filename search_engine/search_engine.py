from flask import Flask, render_template, request
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

app = Flask(__name__, template_folder="./static/")

@app.route("/")
def websearch():
    return render_template("index.html")

@app.route("/peter")
def peter():
    return render_template("a.html")

@app.route("/lois")
def lois():
    return render_template("b.html")

@app.route("/chris")
def chris():
    return render_template("c.html")

@app.route("/meg")
def meg():
    return render_template("d.html")

@app.route("/stewie")
def stewie():
    return render_template("e.html")

@app.route("/websearch", methods = ['GET', 'POST'])
def web_search():
    if request.method == 'POST':
        query = request.form['query']
        if query == "":
            return render_template('index.html')
        websites = [
            'http://localhost:5000/peter',
            'http://localhost:5000/lois',
            'http://localhost:5000/chris',
            'http://localhost:5000/meg',
            'http://localhost:5000/stewie'
        ]
        
        tokenized_text = load_tokenized_text('tokenized_text_pickle.pkl')
        tfidf = TfidfVectorizer()
        tfidf_vectors = tfidf.fit_transform([' '.join(tokens) for tokens in tokenized_text])
        
        query_vector = tfidf.transform([query])
        
        similarities = cosine_similarity(query_vector, tfidf_vectors)
        
        if all_zeros(similarities[0]):
            return render_template('notfound.html')
        
        G = nx.DiGraph()
        
        for i, link in enumerate(websites):
            G.add_node(link)
            for j, sim in enumerate(similarities[0]):
                if sim > 0 and i != j:
                    G.add_edge(link, websites[j], weight = sim)
                    
        pagerank = nx.pagerank(G)
        
        ranked_results = sorted(pagerank.items(), key = lambda x: x[1], reverse = True)
        
        top_results = [x[0] for x in ranked_results if x[1] >= 0.14]
        print(top_results)
        return render_template('results.html', data = [top_results, query])
    
        

def load_tokenized_text(filename):
    tokenized_text = pickle.load(open(filename, 'rb'))
    return tokenized_text


def all_zeros(l):
    for i in l:
        if i != 0:
            return False
        return True

if __name__ == '__main__':
    app.run(debug=True)