from flask import Flask, render_template, request

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
        
        return render_template('results.html', data = query)


if __name__ == '__main__':
    app.run(debug=True)