from flask import Flask, render_template, request
import main_WEB

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/read-form",methods=["POST"])
def read_form():
    data=request.form
    print(data["program"])
    return render_template("output_program.html",output=main_WEB.run_program(False,data["program"]))
@app.route("/form", methods=["GET"])
def fill_out_form():
    return render_template("input_program.html")

app.run(debug=True)