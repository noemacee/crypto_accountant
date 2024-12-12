from flask import Flask, render_template
from flask import request, jsonify
import run


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("./frontend/templates/index.html")


@app.route("/process")
def process():
    data = request.json
    result = run.main()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
