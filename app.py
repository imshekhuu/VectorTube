from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    link = request.form["video_link"]
    return render_template("chat.html", video_url=link)



if __name__ == "__main__":
    app.run(debug=True)