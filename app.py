from flask import Flask,render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL 

app=Flask(__name__)

app.config["MYSQL_HOST"]="127.0.0.1"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="WJ28@krhps"
app.config["MYSQL_DB"]="mathan"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def home():
    try:
        con=mysql.connection.cursor()
        sql="SELECT * FROM gopal"
        con.execute(sql)
        res=con.fetchall()
        return render_template("home.html",datas=res)
    except Exception as e:
        return f"An error occurred: {str(e)}"
        
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        con = mysql.connection.cursor()
        sql = "INSERT INTO gopal(name, age, city) values (%s, %s, %s)"
        con.execute(sql, [name, age, city])
        mysql.connection.commit()
        flash('User Details Added')
        con.close()
        return redirect(url_for("home"))
    return render_template("add.html")
    
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        city = request.form["city"]
        sql = "UPDATE gopal SET name=%s, age=%s, city=%s WHERE id=%s"
        con.execute(sql, (name, age, city, id))
        mysql.connection.commit()
        flash('User Details Updated')
        con.close()       
        return redirect(url_for("home"))
    else:
        sql = "SELECT * FROM gopal WHERE id=%s"
        con.execute(sql, (id,))
        data = con.fetchone()
        con.close()
        return render_template("edit.html", data=data)
        
@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    con = mysql.connection.cursor()
    sql = "DELETE FROM gopal WHERE id=%s"
    con.execute(sql, (id,))
    mysql.connection.commit()
    flash('User Details Deleted')
    con.close()   
    return redirect(url_for("home"))
    
if(__name__=='__main__'):
    app.secret_key="abc123"
    app.run(debug=True)