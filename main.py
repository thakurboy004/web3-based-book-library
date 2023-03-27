from flask import Flask, render_template, request, send_file
from py_filecoin_api_client import FilecoinAPI

app = Flask(__name__)
api = FilecoinAPI("http://localhost:7777/rpc/v0")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_contents = file.read()
    cid = api.client.import_data(file_contents)["import_data_response"]["root"]
    return cid

@app.route("/download/<cid>")
def download(cid):
    file_contents = api.client.read_data(cid)
    return send_file(io.BytesIO(file_contents), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
