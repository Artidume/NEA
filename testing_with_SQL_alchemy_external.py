from testing_with_SQL_alchemy import Users, Programs,Comments, db #import all the Stuffs
from flask import Flask, render_template, request
from sqlalchemy import text
#init db
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aqasm.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)

#create all the tables if not already made:
with app.app_context():
    db.create_all()

def get_user_details(id=None,username=None): #allows to pass in either username, or id, to search for a user.
    if username==id and id==None:
        return "what. no. stop that."
    if username is not None:
        sql_command = text(f"SELECT * FROM Users WHERE username={username};")
        result = 
    

    
    return results


def get_programs(user_id):
    results= Programs.query.filter_by(user_id=user_id).all() #sql: SELECT * from Programs WHERE user_id=(user_id);    (user_id) is the input id
    print(results)
def add_user(username,password):
    encrypted_password=""
    count=1
    for character in password:
        encrypted_password+=chr((ord(character)+count)%26)
        print(encrypted_password)
        count+=1
    new_user=Users(username=username,encrypted_password=encrypted_password)
    db.session.add(new_user) #send a request to add them to the database
    db.session.commit() #commit new user to database

with app.app_context():
    #add_user("jeef","berky")
    print(get_user_details(username="beef"))