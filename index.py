from flask import Flask, render_template, request, jsonify
import ibooks_highlights_exporter as ib
app = Flask(__name__)
res = {}

@app.route("/")
def hello():
    global res
    #ib.get_all_relevant_titles()
    res = ib.get_all_relevant_titles()
    #op = ["<ul>"]

    #for it in res:
        #op.append("<li id='%s'><input type='checkbox' name='titles' value='%s' />%s</li>" % (it["ZASSETID"], it["ZASSETID"], it["ZTITLE"]))

    #op.append("</ul>")

    #return "".join(op)
    return render_template('index.html', booklist=res)

@app.route("/export", methods=['POST'])
def export():
    ts = request.form.getlist('titles')
    res1 = ib.get_all_highlights()
    asset_title_tab = ib.get_asset_title_tab()
    print res1
    print asset_title_tab
    #assetlist = [x[0] for x in request.form]
    return render_template('simpletemplate.html', obj={"last":"###", "date":ib.today, "highlights":res1, "assetlist":asset_title_tab, "notoc":False, "nobootstrap":False})

if __name__ == "__main__":
    app.debug = True
    app.run()
