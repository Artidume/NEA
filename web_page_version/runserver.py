from flask import Flask, render_template
import main_WEB

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",output=main_WEB.run_program(True,"OUTPUT #2\nHALT"))

app.run(debug=True)