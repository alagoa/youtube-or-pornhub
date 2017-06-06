from flask import Flask
import netutils

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "sup mpts"

if __name__ == "__main__":
    app.run(host=netutils.get_lan_ip())