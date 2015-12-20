from flask import Flask, render_template, request, jsonify
import ibooks_highlights_exporter as ib
app = Flask(__name__)
res = {}

@app.route("/")
def hello():
    global res
    res = ib.get_all_titles()
    #op = ["<ul>"]

    #for it in res:
        #op.append("<li id='%s'><input type='checkbox' name='titles' value='%s' />%s</li>" % (it["ZASSETID"], it["ZASSETID"], it["ZTITLE"]))

    #op.append("</ul>")

    #return "".join(op)
    return render_template('index.html', booklist=res)

@app.route("/export", methods=['POST'])
def export():
    print request.form
    print res
    #return jsonify(request.form)
    return render_template('simpletemplate.html', obj={"last":"###", "date":ib.today, "highlights":ib.res1, "assetlist":ib.asset_title_tab, "notoc":False, "nobootstrap":False})

if __name__ == "__main__":
    app.debug = True
    app.run()
