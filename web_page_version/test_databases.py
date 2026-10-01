#designed to align with CRUD (Create, Read, Update, Delete). 
def get_logins():
    with open('web_page_version/databases/login_database.csv') as f:
        line="placeholder"
        output=[]
        while line!=[""]: #while not empty
            line=f.readline().split(",") #read and split by comma
            #this, down to the for loop, just cleans the line into something more useable.
            line_array=[]
            for data_item in line: 
                line_array.append(data_item.strip())
            if line!=[""]:
                output.append(line_array)
                pass
        
        return output #multidimensional array, each item in it is a login with all data from login stored in an array. e.g. [[username1,password1],[username2,password2],...]
def query_user(id): #id:integer
    id=str(id) #make comparison faster, since login[0] will be a string. If I had done int(login[0]) instead, that would be called once for every login. much slower.
    logins = get_logins()
    #could do binary search here but im tired :(
    for login in logins: #linear search
        if login[0]==id:
            return login #return all info about user
    return "NOT FOUND" #searched through all of list, didn't find it! cry.
def add_user(id,username,password): #id:integer, username:string, password:string
    #inputting id as 0 implies add with no specific id in mind. therefore, make id the NEXT id number (autoincrement)
    if id==0:
        accounts=get_logins()
        all_ids_used=[]
        for account in accounts:
            all_ids_used.append(account[0])
        #print(all_ids_used)
        new_id=1
        for i in range(0,len(accounts)+1):
            if str(new_id) in all_ids_used:
                new_id+=1
        id=new_id

    #basic error handling for Funky Stuff That Will Not Be Good
    #print("step1")
    if id is None or username is None or password is None:
        return "ERROR: Missing parameter"
    if " " in username:
        return "ERROR: Username cannot contain spaces."
    if " " in password:
        return "ERROR: Password cannot contain spaces."
    #ensure id is unique
    #print("step2")
    accounts=get_logins()
    if accounts==[]: #empty
        continue_validation=False#since no accounts stored, no problem!
    else:
        continue_validation=True
    
    id_is_unique=True
    username_is_unique=True
    if continue_validation:
        for account in accounts:
            if account[0]==id:
                id_is_unique=False
            if account[1]==username:
                username_is_unique=False
    #print("step3")



    if id_is_unique and username_is_unique:
        #print(id,username,password)
        with open("web_page_version/databases/login_database.csv","a") as f:
            f.write(f"{id}, {username}, {password}\n")
    else:
        if id_is_unique:
            print("error with username.")
        else:
            print("error with id.")
    return 0
def delete_user(id): #id:integer
    #this technique involves reading the file, and then rewriting the file for everything excluding the account for that id. takes O(n) time (technically O(2n) but that's not how notation works)
    accounts=get_logins()
    with open("web_page_version/databases/login_database.csv","w") as f:
        f.write("")
    for line in accounts:
        if line[0]!=str(id):
            add_user(line[0],line[1],line[2]) #add back every user that does not have the deleted user id.
    

    
if __name__=="__main__":
    add_user(0,"guy3345333","password")
    add_user(0,"pok","pokpok")
    add_user(0,"5u|)3RH4XX0R","password123")
    delete_user(1)
    print(get_logins())