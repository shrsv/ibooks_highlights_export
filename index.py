from flask import Flask
import ibooks_highlights_exporter as ib
app = Flask(__name__)

@app.route("/")
def hello():
    res = ib.get_all_titles()
    return "<br />".join(res)

if __name__ == "__main__":
    app.run()
