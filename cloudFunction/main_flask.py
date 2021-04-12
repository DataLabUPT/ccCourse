from flask import Flask
from flask import make_response
from flask import request
from generareDeclaratie import generare_declaratie

app = Flask(__name__)


@app.route("/")
def index():
    return 'Index Page'


@app.route('/declaratie/', methods=['POST'])
def declaratie():
    req_data = request.get_json()
    response = make_response(generare_declaratie(req_data))
    response.headers.set('Content-Disposition', 'attachment', filename='form.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

if __name__ == "__main__":
    app.run(debug=True)
