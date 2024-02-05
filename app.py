from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId  

app = Flask(__name__, template_folder='template')
# admin login data
client = MongoClient('mongodb://localhost:27017/')
db = client['User_db']
users_collection = db['users']
# client login data 
client1 = MongoClient('mongodb://localhost:27017/')
db = client['Client_db']
client_collection = db['client']

@app.route('/')
def index():
    return render_template('Main.html')
#ADMIN LOGIN SIGN UP AND DASHBOARD 
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            'username': request.form['txt'],
            'email': request.form['email'],
            'CompanyDomain': request.form['cmpDomain'],
            'City': request.form['city'],
            'Mobile_No': request.form['phn'],
            'PINCODE': request.form['pin'],
            'State': request.form['state'],
            'password': request.form['pswd']
        }
        users_collection.insert_one(user_data)
        return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']

        user = users_collection.find_one({'email': email, 'password': password})

        if user:
            return redirect(url_for(endpoint="dashboard", user_data=user))
        else:
            return "Login failed"

@app.route('/signup')
def signup1():
    return render_template('signup.html')

@app.route('/login')
def login1():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_data = request.args.get('user_data')
    if user_data:
        user_data = eval(user_data)  
        return render_template('dashboard.html', user_data=user_data)
    else:
        return "User data not found"
# CLIENT LOGIN SIGNUP DASHBOARD   
@app.route('/client_signup', methods=['POST'])
def client_signup():
    if request.method == 'POST':
        client_data = {
            'username': request.form['txt'],
            'email': request.form['email'],
            'City': request.form['city'],
            'Mobile_No': request.form['phn'],
            'PINCODE': request.form['pin'],
            'State': request.form['state'],
            'password': request.form['pswd']
        }
        client_collection.insert_one(client_data)
        return redirect(url_for('client_login'))

@app.route('/client_login', methods=['POST'])
def client_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pswd']

        # Change the variable name to avoid conflict
        client_user = client_collection.find_one({'email': email, 'password': password})

        if client_user:
            return redirect(url_for(endpoint="client_dashboard", client_data=client_user))
        else:
            return "Login failed"
        

@app.route('/client_dashboard')
def client_dashboard():
    client_data = request.args.get('client_data')
    if client_data:
        client_data = eval(client_data)  
        return render_template('client_dashboard.html', client_data=client_data)
    else:
        return "User data not found"


@app.route('/client_signup')
def signup2():
    return render_template('client_signup.html')

@app.route('/client_login')
def login2():
    return render_template('client_login.html')

@app.route('/user_search')
def user_search():
    return render_template('user_search.html')
@app.route('/user_search', methods=['POST'])
def  admin_search():
        if request.method == 'POST':
         search_criteria = {
            'username': request.form.get('txt'),
            'email': request.form.get('email'),
            'CompanyDomain': request.form.get('cmpDomain'),
            'City': request.form.get('city'),
            'Mobile_No': request.form.get('phn'),
            'PINCODE': request.form.get('pin'),
            'State': request.form.get('state'),
            'password': request.form.get('pswd')
        }

        # Constructing a query based on the provided inputs
        query = {}
        for key, value in search_criteria.items():
            if value:
                query[key] = value

        # Performing the search in MongoDB
        search_results = list(users_collection.find(query))
        # if search_results:
        #  search_results = eval(search_results)  
       
        print("hello")
        print(search_results)

        # You can now use 'search_results' to display or process the matching records
        return render_template('user_search.html', results=search_results)

    
    

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
