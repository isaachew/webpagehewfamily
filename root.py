from flask import Flask, render_template, request, redirect, Response
import requests
app = Flask(__name__)
from hashlib import sha256
try:
    import cPickle as pickle
except:
    import pickle
from datetime import datetime
import json,random,os
data = {'comments': [], "passwords":{"Isaac":['fd2c1b2071df9fc4fddbe43eaeb6d0eb5a95e23fac32d8ad4fc036593d8bb41b',1]}, "tabs":[]}
password=[]
def save_db():
    f=open('data.json','w')
    f.write(json.dumps(data))
def load_db():
    global data
    fp=open('data.json','r')
    d = json.loads(fp.read())
    fp.close()
    for key in data:
        if key not in d:
            d[key] = data[key]
    data = d
try:
    load_db()
    bad=False
except:
    print("error loading")
    save_db()
    load_db()
@app.route("/a")
def a():
    s=""
    for i in range(20):
       s+=chr(random.randint(0,255))
    return s
@app.route('/comment', methods=['POST'])
def comment():
    global data
    if "new" in request.form.getlist("new"):
        if request.form["name"] not in data["passwords"]:
            data["passwords"][request.form["name"]]=[sha256(request.form["pwd"]).hexdigest(),False]
        else:
            return redirect("/?login=3")
    if request.form["name"] not in data["passwords"]:
        return redirect("/?login=2")
    if data["passwords"][request.form["name"]][0] == sha256(request.form["pwd"]).hexdigest():
        data["comments"].append({"tab":int(request.form["tab"]),"uid":request.form["name"],"comment":request.form["comment"],"time":str(datetime.now())+" UTC"+(" This is an admin posting."*int(data["passwords"][request.form["name"]][1]))})
        save_db()
        return redirect("/")
    else:
        return redirect("/?login=1")
@app.route("/adminw",methods=["POST"])
def admin():
    if sha256(request.form["passwd"]).hexdigest() in password:
        return render_template("admin.html",comm=json.dumps(data))
    else:
        return redirect("/")

@app.route("/admin")
def passwdget():
    global password
    for a in data["passwords"].items():
        if a[1][1]==1:
         password+=[a[1][0]]
    return """
    <title>Admin Password Confirmation</title>
    <form action = "/adminw" method = "post">
        Enter the admin password:<input name="passwd" type="password">
        <input type="submit" value="Go to admin">
    </form>
    """
@app.route("/trap/<int:a>")
def trap(a=1):
    return "<a href='/trap/"+str(a+1)+"'>Spider trap. To /trap/"+str(a+1)+"</a>"
@app.route('/')
def index(v=None):
    if request.headers.get('X-Forwarded-Proto', 'http')=='http':
        url="https"+request.url[4:]
        if url.endswith(":80/"):
            url=url[:-1]
            url+="80"
        return redirect(url)
    tindex=sum([i+1 if " & ".join(data["tabs"][i]["owners"])==v else 0 for i in range(len(data["tabs"]))])-1
    if tindex==-1 and v!=None:
        return render_template("nf.html")
    return render_template("index.html",data=data,v=sum([i+1 if " & ".join(data["tabs"][i]["owners"])==v else 0 for i in range(len(data["tabs"]))])-1)
@app.route("/changecomments",methods=["POST"])
def change():
    global data
    dat=json.loads(request.form["comments"])
    data["tabs"]=dat["tabs"]
    data["comments"]=dat["comments"]
    save_db()
    return redirect("/")
@app.route("/hash",methods=["POST"])
def hash():
    if sha256(request.form["pwd"]).hexdigest() in password:
        return sha256(request.form["n"]).hexdigest()
    else:
        return redirect("/")
@app.errorhandler(404)
def t(n):
    return render_template("nf.html"),404
@app.errorhandler(405)
def t405(n):
    return render_template("nf.html"),405
@app.route("/tabs")
def editlogin():
    return render_template("edlog.html")
@app.route("/edittabs",methods=["POST"])
def edittabs():
    try:
        if sha256(request.form["pwd"]).hexdigest()==data["passwords"][request.form["name"]][0]:
            resp=Response(render_template("tabs.html",data=data))
            resp.headers['Cache-Control'] = 'no-cache'
            normdata=filter(lambda x:request.form["name"] in x["owners"],data["tabs"])
            if data["passwords"][request.form["name"]][1]:
                dat=data["tabs"]
            else:
                dat=normdata
            return render_template("tabs.html",data={"tabs":dat,"fonts":data["fonts"]})
    except KeyError:
        pass
    return redirect("/")
@app.route("/apple-touch-icon.png")
def appleicon():
    return redirect("/static/img/ico144.png")
@app.route("/servw.js")
def servw():
    rt=os.path.join(os.path.dirname(os.path.abspath(__file__)),"servw.js")
    f=open(rt)
    a=f.read()
    f.close()
    return Response(a,mimetype="text/javascript")
@app.route("/robots.txt")
def robots():
    rt=os.path.join(os.path.dirname(os.path.abspath(__file__)),"static/robots.txt")
    f=open(rt)
    a=f.read()
    f.close()
    return Response(a,mimetype="text/plain")
@app.route("/fonts")
def fonts():
    return Response(requests.get("https://fonts.googleapis.com/css?"+"&".join([n[0]+"="+n[1] for n in request.args.items()])).content,mimetype="text/css")
@app.route("/changetabs",methods=["POST"])
def changets():
    global data
    d=json.loads(request.form["tabs"])
    for i in d:
        for j in range(len(data["tabs"])):
            print(j,"old",data["tabs"][j]["owners"],'new',i["owners"],'"')
            if data["tabs"][j]["owners"]==i["owners"]:
                data["tabs"][j]=i
    save_db()
    return redirect("/")
@app.route("/<v>")
def details(v):
    return index(v)
app.run(host="0.0.0.0",port=8080,debug=True)