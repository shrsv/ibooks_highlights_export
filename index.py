from flask import Flask, render_template
import ibooks_highlights_exporter as ib
app = Flask(__name__)

@app.route("/")
def hello():
    res = ib.get_all_titles()
    #op = ["<ul>"]

    #for it in res:
        #op.append("<li id='%s'><input type='checkbox' name='titles' value='%s' />%s</li>" % (it["ZASSETID"], it["ZASSETID"], it["ZTITLE"]))

    #op.append("</ul>")

    #return "".join(op)
    return render_template('index.html', booklist=res)

if __name__ == "__main__":
    app.debug = True
    app.run()
