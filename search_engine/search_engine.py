from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello_world():
    return "<p>Hello, World</p>"

@app.route("/about")
def about():
    return "<h1>About</h1>"

if __name__ == '__main__':
    app.run(debug=True)