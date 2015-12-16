from flask import Flask
import ibooks_highlights_exporter as ib
app = Flask(__name__)

@app.route("/")
def hello():
    res = ib.get_all_titles()
    op = ["<ul>"]

    for it in res:
        print it
        op.append("<li id='%s'>%s</li>" % (it["ZASSETID"], it["ZTITLE"]))

    op.append("</ul>")

    return "".join(op)

if __name__ == "__main__":
    app.debug = True
    app.run()
