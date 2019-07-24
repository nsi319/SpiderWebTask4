from flask import Flask,render_template,request,redirect,url_for,session
from flaskext.mysql import MySQL
from datetime import date

app=Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movies'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)
app.secret_key="nokey"

@app.route('/signup',methods=['GET','POST'])
def signup():
    conn=mysql.connect()
    cur=conn.cursor()
    msg=None

    if request.method=='POST':
        password=request.form.get("pass")
        username=request.form.get("user")
        passc=request.form.get("passc")

        cur.execute('''SELECT * FROM users WHERE username=%s''',(username))
        u=cur.fetchone()

        if u is None:
            if passc!=password:
                msg="Passwords do not match"
            else:
                cur.execute('''INSERT INTO users VALUES (%s,%s,%s)''',(username,password,"public"))
                conn.commit()
                msg="User created. Login for further use"
        else:
            msg="Username already taken"
    return render_template('register.html',msg=msg)

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    conn=mysql.connect()
    cur=conn.cursor()
    msg=None

    if request.method=='POST':
        password=request.form.get("pass")
        username=request.form.get("user")
        cur.execute('''SELECT * FROM users WHERE username=%s''',(username))
        data=cur.fetchone()
        if data is None or password!=data[1]:
            msg="Invalid username or password"
        else: 
            session['user']=username
            return redirect(url_for('home'))    
    return render_template("login.html",msg=msg)

@app.route('/home',methods=['GET','POST'])
def home():
    if request.method=='POST':
        value=request.form.get('search')
        return redirect(url_for('view',value=value))

    return render_template('home.html')

@app.route('/view/<value>')
def view(value):
    conn=mysql.connect()
    cur=conn.cursor()
    cur.execute('''SELECT * FROM comments WHERE title=%s''',(value))
    comment=cur.fetchall()
    k=0
    comments = []
    i=len(comment)-1
    while i>=0 :
        comments.append(comment[i])
        k=k+1
        i=i-1

    return render_template('view_movie.html',value=value,comments=comments)

@app.route('/profile',methods=['GET','POST'])
def profile():
    conn=mysql.connect()
    cur=conn.cursor()
    msg=""
    if request.method=='POST':
        username=request.form.get('username')
        return redirect(url_for('viewprofile',user=username))
    
    cur.execute('''SELECT * FROM liked WHERE username=%s''',(session['user']))
    data=cur.fetchall()
    cur.execute('''SELECT * FROM watchlater WHERE username=%s''',(session['user']))
    data1=cur.fetchall()
    cur.execute('''SELECT * FROM watched WHERE username=%s''',(session['user']))
    data2=cur.fetchall()
    cur.execute('''SELECT * FROM favourites WHERE username=%s''',(session['user']))
    data3=cur.fetchall()
    cur.execute('''SELECT * FROM users WHERE username=%s''',(session['user']))
    t=cur.fetchone()

    return render_template('profile.html',data=data,data1=data1,data2=data2,data3=data3,type=t[2])

@app.route('/viewprofile/<user>')
def viewprofile(user):
    conn=mysql.connect()
    cur=conn.cursor()
    msg=None
    cur.execute('''SELECT * FROM users WHERE username=%s''',(user))
    u=cur.fetchone()
    if u is None:
        msg="No user exsits"
        return render_template('users.html',msg=msg)
    elif u[2]=="private":
        msg="Private account..cannot see acivity"
        return render_template('users.html',msg=msg)
    else:
        cur.execute('''SELECT * FROM liked WHERE username=%s''',user)
        data=cur.fetchall()
        cur.execute('''SELECT * FROM watchlater WHERE username=%s''',user)
        data1=cur.fetchall()
        cur.execute('''SELECT * FROM watched WHERE username=%s''',user)
        data2=cur.fetchall()
        cur.execute('''SELECT * FROM favourites WHERE username=%s''',user)
        data3=cur.fetchall()
        cur.execute('''SELECT * FROM users WHERE username=%s''',user)
        t=cur.fetchone()
        return render_template('users.html',data=data,data1=data1,data2=data2,data3=data3,type=t[2],msg=msg)

@app.route("/like",methods=['GET','POST'])
def like():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        st=request.form.get('state')
        path=request.form.get('path')
        title=request.form.get('title')
        if st=="liked":
            cur.execute('''INSERT INTO liked VALUES (%s,%s,%s)''',(session['user'],title,path))
            conn.commit()
            return "added"
        elif st=="disliked":
            cur.execute('''DELETE FROM liked WHERE username=%s AND title=%s AND path=%s''',(session['user'],title,path))
            conn.commit()
            return "removed"


@app.route("/favouites",methods=['GET','POST'])
def favourites():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        st=request.form.get('state')
        path=request.form.get('path')
        title=request.form.get('title')
        if st=="fa":
            cur.execute('''INSERT INTO favourites VALUES (%s,%s,%s)''',(session['user'],title,path))
            conn.commit()
            return "added"
        elif st=="nfa":
            cur.execute('''DELETE FROM favourites WHERE username=%s AND title=%s AND path=%s''',(session['user'],title,path))
            conn.commit()
            return "removed"

@app.route("/watchlater",methods=['GET','POST'])
def watchlater():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        st=request.form.get('state')
        path=request.form.get('path')
        title=request.form.get('title')
        if st=="wl":
            cur.execute('''INSERT INTO watchlater VALUES (%s,%s,%s)''',(session['user'],title,path))
            conn.commit()
            return "added"
        elif st=="rwl":
            cur.execute('''DELETE FROM watchlater WHERE username=%s AND title=%s AND path=%s''',(session['user'],title,path))
            conn.commit()
            return "removed"    

@app.route("/watched",methods=['GET','POST'])
def watched():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        st=request.form.get('state')
        path=request.form.get('path')
        title=request.form.get('title')
        if st=="wa":
            cur.execute('''INSERT INTO watched VALUES (%s,%s,%s)''',(session['user'],title,path))
            conn.commit()
            return "added"
        elif st=="nwa":
            cur.execute('''DELETE FROM watched WHERE username=%s AND title=%s AND path=%s''',(session['user'],title,path))
            conn.commit()
            return "removed" 

@app.route('/addcomment',methods=['GET','POST'])
def addcomment():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        comment=request.form.get('comment')
        title=request.form.get('title')
        cur.execute('''INSERT INTO comments VALUES(%s,%s,%s)''',(session['user'],comment,title))
        conn.commit()
        return "added"

@app.route('/acctype' , methods=['GET','POST'])
def acctype():
    conn=mysql.connect()
    cur=conn.cursor()
    if request.method=='POST':
        actype=request.form.get('state')
        cur.execute('''UPDATE users SET type=%s WHERE username=%s''',(actype,session['user']))
        conn.commit()
        return "changed"

if __name__ == '__main__':
    app.run(debug=True)

