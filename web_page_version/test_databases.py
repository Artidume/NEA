#designed to align with CRUD (Create, Read, Update, Delete). 
def get_logins():
    with open('web_page_version/databases/login_database.csv') as f:
        line="placeholder"
        output=[]
        while line!=[""]: #while not empty
            line=f.readline().split(",") #read and split by comma
            line_array=[]
            for data_item in line: 
                line_array.append(data_item.strip()) #clean line to make it easier to use
            if line!=[""]:
                output.append(line_array)
                pass
        
        return output #multidimensional array, each item in it is a login with all data from login stored in an array. e.g. [[id1,username1,password1],[id2,username2,password2],...]
def delete_all_users():
    accounts=get_logins()
    print("SCRAW!!!!!!!!!!!!!!!!!!!!")
    print(accounts)
    for account in accounts:
        delete_user(int(account[0]))




def query_user(id): #id:integer
    id=str(id) #make comparison faster, since login[0] will be a string. If I had done int(login[0]) instead, that would be called once for every login. much slower.
    logins = get_logins()
    #could do binary search here but im tired :(
    for login in logins: #linear search
        if login[0]==id:
            return login #return all info about user
    return "NOT FOUND" #searched through all of list, didn't find it! cry.
def add_user(username,password): #username:string, password:string
    #basic error handling
    if username is None or password is None:
        return "ERROR: Missing parameter"
    if " " in username:
        return "ERROR: Username cannot contain spaces."
    if " " in password:
        return "ERROR: Password cannot contain spaces."
    accounts=get_logins()
    if accounts==[]: #empty
        continue_validation=False#since no accounts stored, no problem!
    else:
        continue_validation=True
    
    
    username_is_unique=True
    if continue_validation:
        highest_id=0
        for account in accounts:
            if account[1]==username:
                username_is_unique=False
            if int(account[0])>highest_id:
                highest_id=int(account[0])
        id=highest_id+1
    else:
        id=1



    if username_is_unique:
        #print(id,username,password)
        with open("web_page_version/databases/login_database.csv","a") as f:
            f.write(f"{id}, {username}, {password}\n")
    else:
        print("username is not unique")
    return 0
def delete_user(id): #id:integer
    #this technique involves reading the file, and then rewriting the file for everything excluding the account for that id. takes O(n) time (technically O(2n) but that's not how notation works)
    accounts=get_logins()
    with open("web_page_version/databases/login_database.csv","w") as f:
        f.write("")
    for line in accounts:
        if line[0]!=str(id):
            add_user(line[1],line[2]) #add back every user that does not have the deleted user id.
    

    
if __name__=="__main__": #debugging the database can be done in here. Remember an id of 0 is autoassigned to the "next" free space.
    #for i in range(0,100):
    #    add_user(str(i),"password123")
    delete_all_users()
    '''
    print(get_logins())
    delete_all_users()
    print("SCRAW")
    print(get_logins())
    '''