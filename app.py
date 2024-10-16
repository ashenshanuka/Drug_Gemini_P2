from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  # Import for database connection

app = Flask(__name__)

# MySQL connection (Replace details with your actual credentials)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="pharmacy_gemini_02_db"
)
mycursor = mydb.cursor()

# Home page
@app.route("/")
def index():
    return render_template("index.html")  # Assuming you have an index.html

# Add drug
@app.route("/add_drug", methods=["GET", "POST"])
def add_drug():
    if request.method == "POST":
        name = request.form["name"]
        stock = request.form["stock"]
        cost = request.form["cost"]
        shelf_life = request.form["shelf_life"]
        # Insert data into the database
        sql = "INSERT INTO drugs (name, stock, cost, shelf_life) VALUES (%s, %s, %s, %s)"
        val = (name, stock, cost, shelf_life)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for("index"))
    return render_template("add_drug.html")

# Browse drugs
@app.route("/browse_drugs")
def browse_drugs():
    # Fetch data from the database
    sql = "SELECT * FROM drugs"
    mycursor.execute(sql)
    drugs = mycursor.fetchall()
    return render_template("browse_drugs.html", drugs=drugs)

# Search drugs
@app.route("/search_drugs", methods=["GET", "POST"])
def search_drugs():
    if request.method == "POST":
        search_query = request.form["search_query"]
        # Search for drugs based on name or ID
        sql = "SELECT * FROM drugs WHERE name LIKE %s OR id = %s"
        val = ("%{}%".format(search_query), search_query)
        mycursor.execute(sql, val)
        drugs = mycursor.fetchall()
        return render_template("search_drugs.html", drugs=drugs)
    return render_template("search_drugs.html")

# Edit drug
@app.route("/edit_drug/<int:id>", methods=["GET", "POST"])
def edit_drug(id):
    # Fetch existing drug data
    mycursor = mydb.cursor(dictionary=True)  # Use DictCursor
    sql = "SELECT * FROM drugs WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    drug = mycursor.fetchone() 
    if request.method == "POST":
        name = request.form["name"]
        stock = request.form["stock"]
        cost = request.form["cost"]
        shelf_life = request.form["shelf_life"]
        # Update drug data
        sql = "UPDATE drugs SET name = %s, stock = %s, cost = %s, shelf_life = %s WHERE id = %s"
        val = (name, stock, cost, shelf_life, id)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for("browse_drugs"))  # Redirect to browse after update
    return render_template("edit_drug.html", drug=drug)

# Delete drug
@app.route("/delete_drug/<int:id>")
def delete_drug(id):
    # Delete drug data
    sql = "DELETE FROM drugs WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("browse_drugs"))

if __name__ == "__main__":
    app.run(debug=True)