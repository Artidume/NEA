from flask import Flask, render_template, request
import main_WEB
import sqlite3 #used for database handling
#init database


def sqlite3_command_non_output(command):
    con=sqlite3.connect("NEA_DATABASE.db")
    cursor=con.cursor()
    try:
        cursor.execute(command)
        con.commit()
    finally:
        cursor.close()
        con.close()

def sqlite3_command_output(command):
    con=sqlite3.connect("NEA_DATABASE.db")
    cur=con.cursor()
    try:
        cur.execute(command)
        results=[]
        for result in cur:
            results.append(result)
    finally:
        if results is None:
            results=[]
        cur.close()
        con.close()
    return results
#sqlite3_command_non_output("INSERT INTO users VALUES('test','test2',3)")
#print(sqlite3_command_output("SELECT * FROM users"))

#init webserver
app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/output",methods=["POST"])
def read_form():
    data=request.form
    try:
        if data["debug_flag"] == "True":
            debug_flag=True
        else:
            debug_flag=False
    except:
        debug_flag=False
    
    return render_template("output_program.html",output=main_WEB.run_program(debug_flag,data["program"]))

@app.route("/program", methods=["GET"])
def fill_out_form():
    return render_template("input_program.html")

@app.route("/program-debug", methods=["GET"])
def fill_out_but_debug_this_time_now_wow_okay_cool_thanks_okay_awesome_cheers_mate():
    return render_template("input_program_debug.html")

@app.route("/output-debug",methods=["POST"])
def output_debug():
    data=request.form
    #print(data["program"])
    output=main_WEB.run_program(True,data["program"])
    #print(output)
    return render_template("output_program.html",output=output)
app.run(debug=True,host="0.0.0.0", port=5000) #run server