from flask import Flask, render_template, request
import main_WEB

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/output",methods=["POST"])
def read_form():
    data=request.form
    print(data["program"])
    return render_template("output_program.html",output=main_WEB.run_program(False,data["program"]))

@app.route("/program", methods=["GET"])
def fill_out_form():
    return render_template("input_program.html")

@app.route("/program-debug", methods=["GET"])
def fill_out_but_debug_this_time_now_wow_okay_cool_thanks_okay_awesome_cheers_mate():
    return render_template("input_program_debug.html")

@app.route("/output-debug",methods=["POST"])
def output_debug():
    data=request.form
    print(data["program"])
    output=main_WEB.run_program(True,data["program"])
    print(output)
    return render_template("output_program.html",output=output)
app.run(debug=True)