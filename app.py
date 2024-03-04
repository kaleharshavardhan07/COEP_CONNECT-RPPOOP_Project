from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash
from pymongo import MongoClient
from bson import ObjectId  
from datetime import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__, template_folder='template')
# admin login data
client = MongoClient('mongodb://localhost:27017/')
db = client['User_db']
users_collection = db['users']
# posts_data storage
client = MongoClient('mongodb://localhost:27017/')
db = client['Post_db']
post_collection = db['Posts']
app.secret_key = 'your_secret_key'
#notfiaction database
db = client['notice_system']
notifications_collection = db['notifications']

app.config["MONGO_URI"] = "mongodb://localhost:27017/interests"
mongo = PyMongo(app)

CHOICES = [
    'Drama and Film Club',
    'Boat Club',
    'Civil Services Aspirants Club',
    'Janeev Club',
    'HAM Club',
    'Astronomy Club',
    'Science Club',
    'History Club',
    'Personality Development club',
    'Google Student Club',
    'Cultural Club',
    'Debate Club',
    'Ramanujan Mathematics Club',
    'Arts and Crafts',
    'Aarya Raas',
    'COEP Philomystics',
    'CSAT',
    'Robotics Study CLub',
    'Aerial Robot Study Circle (ARSC)',
    'Spic Macay',
    'CSI',
    'DSAI',
    'COFSUG',
    'COEP Mitra',
    'Cricket',
    'Field Hockey',
    'Badminton',
    'Football',
    'Tennis',
    'Kabaddi',
    'Wrestling',
    'Table Tennis',
    'Basketball',
    'Volleyball',
    'Athletics',
    'Boxing',
    'Shooting',
    'Chess',
    'Golf',
    'Squash',
    'Cycling',
    'Swimming',
    'Martial Arts',
    'Archery',
    'Snooker',
    'Gymnastics',
    'Rowing',
    'Rugby',
    'Weightlifting',
    'Equestrian',
    'Polo',
    'Billiards',
    'Fencing',
    'Sailing',
    'Reading',
    'Writing',
    'Cooking',
    'Traveling',
    'Photography',
    'Painting',
    'Gardening',
    'Hiking',
    'Playing musical instruments',
    'Playing sports',
    'Yoga and meditation',
    'Watching movies',
    'Gaming',
    'Birdwatching',
    'Astronomy',
    'DIY projects',
    'Crafting',
    'Knitting or crocheting',
    'Volunteering',
    'Learning new languages',
    'Collecting stamps',
    'Collecting coins',
    'Collecting antiques',
    'Fashion and styling',
    'Music concerts',
    'Music festivals',
    'Wine tasting',
    'Home decor',
    'Sustainable living practices',
    'History',
    'Archaeology',
    'Fishing',
    'Scuba diving',
    'Food tasting',
    'Exploring different cuisines',
    'Stand-up comedy',
    'Tea ceremonies',
    'Interior design',
    'Camping',
    'Poetry',
    'Board games',
    'Puzzles',
    'Writing poetry',
    'Writing lyrics',
    'Acting',
    'Dancing',
    'Singing',
    'Motorcycling',
    'Beekeeping',
    'Robotics',
    'Pottery',
    'Calligraphy',
    'Paragliding',
    'Rock climbing',
    'Wine making',
    'Horseback riding',
    'Target shooting',
    'Magic tricks',
    'Origami',
    'Surfing',
    'Snowboarding',
    'Skiing',
    'Rafting',
    'Bungee jumping',
    'Skateboarding',
    'Longboarding',
    'Metal detecting',
    'Space exploration',
    'Cosplay',
    'Cosmetics',
    'Makeup tutorials',
    'Hair styling',
    'Bodybuilding',
    'CrossFit',
    'Mountain biking',
    'Road cycling',
    'Urban exploring',
    'Environmental activism',
    'Wildlife photography',
    'Animal rescue',
    'Pet grooming',
    'Dog training',
    'Cat training',
    'Horse training',
    'Pet adoption',
    'Exotic pets',
    'Reptiles',
    'Amphibians',
    'Marine biology',
    'Coral reef conservation',
    'Deep-sea diving',
    'Underwater photography',
    'Marine conservation',
    'Bird photography',
    'Bird watching'
]

# def get_user_interests(user_id):
#     user_data = mongo.db.user_interests.find_one({"_id": user_id})
#     if user_data:
#         return np.array([user_data[choice] for choice in CHOICES])
#     else:
#         return None

# def get_next_user_id():
    
#     counter_doc = mongo.db.id_counter.find_one_and_update(
#         {"_id": "user_id_counter"},
#         {"$inc": {"seq": 1}},
#         upsert=True,
#         return_document=True
#     )
#     return counter_doc['seq']
@app.route('/connect', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        requirements = request.form.getlist('requirement')
        user_requirements = np.array([1 if choice in requirements else 0 for choice in CHOICES])
    else:
        user_requirements = np.zeros(len(CHOICES)) 
    
    all_users_interests = []
    all_user_ids = []
    for user_data in mongo.db.user_interests.find():
        all_user_ids.append(user_data['_id'])
        interests = [user_data[choice] for choice in CHOICES]
        all_users_interests.append(interests)
    all_users_interests = np.array(all_users_interests)
    similarities = cosine_similarity([user_requirements], all_users_interests)[0]
    compatible_users_data = [{'user_id': user_id, 'similarity': similarity} for user_id, similarity in zip(all_user_ids, similarities)]
    compatible_users_data.sort(key=lambda x: x['similarity'], reverse=True)
    return render_template('connect_people.html', compatible_users=compatible_users_data)

@app.route('/submit', methods=['POST'])
def submit1():
    interests = request.form.getlist('interest')
    user_data = {choice: 0 for choice in CHOICES}
    for interest in interests:
        if interest in CHOICES:
            user_data[interest] = 1
    user_id = session['user_id']
    user_data['_id'] = user_id
    mongo.db.user_interests.insert_one(user_data)
    return redirect('/profile')


@app.route('/Send_notification')
def notify():
    return render_template('notifications.html')

@app.route('/send_request', methods=['POST'])
def send_request():
    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']
    # Save connection request in the database
    notification = {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': 'Connection Request',
        'is_read': False,
        'timestamp': datetime.utcnow()
    }
    notifications_collection.insert_one(notification)
    return 'Connection request sent successfully'

@app.route('/notifications')
def notifications():
    user_id = session['user_id']
    # Query unread notifications for the user
    notifications = notifications_collection.find({'receiver_id': user_id, 'is_read': False})
    return render_template('notifications.html', notifications=notifications)

@app.route('/mark_as_read', methods=['POST'])
def mark_as_read():
    notification_ids = request.form.getlist('notification_ids')
    for notification_id in notification_ids:
        notifications_collection.update_one({'_id': ObjectId(notification_id)}, {'$set': {'is_read': True}})
    return 'Notifications marked as read'

# CONTROL LOGOUT BY TEJAS WORKING  
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
# FUNCTION    
def find_year(mis):
            if mis.startswith("6122"):
                year="Second Year"
                return year
            elif mis.startswith("6123"):
                year="First Year"
                return year
            elif mis.startswith("1121"):
                year="Third Year"
                return year
            elif mis.startswith("1120"):
                 year="Final Year"
                 return year
            elif mis.startswith("6422"):
                 year="Second Year"
                 return year
            elif mis.startswith("6423"):
                 year="First Year"
                 return year
            elif mis.startswith("1421"):
                 year="Third Year"
                 return year
            elif mis.startswith("1420"):
                 year="Final  Year"
                 return year
             
def find_branch(mis):
        if mis[5]=='1':
            branch="CIVIL"
            return branch
        elif mis[5]=='3'and mis[4]=='0':
            branch="COMPUTER"
            return branch
        elif mis[5]=='5':
            branch="ELECTRICAL"
            return branch
        elif mis[5]=='7':
            branch="ENTC"
            return branch
        elif mis[5]=='9':
            branch="INSTRU"
            return branch
        elif mis[5]=='3'and mis[4]=='1':
            branch="MANUFACTURING"
            return branch
        elif mis[5]=='0':
            branch="MECHANICAL"
            return branch
        elif mis[5]=='1'and mis[4]=='1':
            branch="METALLARGY"
            return branch
        elif mis[5]=='4'and mis[4]=='1':
            branch="PLANNING"
            return branch
# INDEX HOME PAGE 
@app.route('/')
def index1():
    return render_template('Main.html')
# LOGIN SIGN UP 
@app.route('/signup', methods=['POST'])
def signup():
    
    if request.method == 'POST':
        mis=request.form['MISNO']
        branch=find_branch(mis)
        year=find_year(mis)
    else:
        return "Unknown", "Unknown"
    user_data = {
            'username': request.form['NAME'],           
            'MIS_NO': request.form['MISNO'],
            'email': request.form['EMAIL'],
            'Mobile_No': request.form['MO_NO'],
            'password': request.form['pswd'],
            'branch': branch,
            'year':year
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
            session['user_id'] = str(user['_id'])
            if 'data_field' in user: 
                if  user['data_field']:  # Check if profile data exists
                
                    return redirect(url_for('main_feed'))
                else:
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('profile'))
        else:
            return "Login failed"

@app.route('/signup')
def signup1():
    return render_template('signup.html')

@app.route('/login')
def login1():
    return render_template('login.html')

# PROFILE CREATION OF LOGIN USER 
@app.route ('/profile')
def profile():
    return render_template('./profile_create.html')
@app.route('/profile', methods=['POST'])
def submit():
    if 'user_id' in session:
        user_id = session['user_id']
        
        data = request.json.get('data')
        if data is not None:
            try:
                users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'data_field': data}})
                return redirect(url_for('main_feed'))
            except Exception as e:
                return f"An error occurred: {str(e)}"
        else:
            return 'No data received'
    else:
        return redirect('/signin')




@app.route('/myprofile')
def myprof():
    if 'user_id' in session:
        
        user_data = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        
        if user_data:
            
            return render_template('myProfile.html', user_data=user_data)
        else:
            
            return "User data not found"
    else:
        
        return redirect(url_for('login'))


@app.route('/myInterest')
def myinter():
    return render_template('interest.html')
    
@app.route('/myConnections')
def myconnect():
    return render_template('connection.html')
    
@app.route('/changePass')
def mypass():
    return render_template('change_pass.html')

from flask import request, redirect, url_for, flash

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user not logged in
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Fetch user data from MongoDB
        user_data = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        print(user_data['password'])
        print(session['user_id'])
        # Verify current password
        if not user_data or not user_data['password']==current_password:
            flash('Current password is incorrect. Please try again.', 'error')
            return redirect(url_for('mypass'))
        
        # Check new passwords match
        if new_password != confirm_password:
            flash('New password and confirm password do not match. Please try again.', 'error')
            return redirect(url_for('mypass'))
        
        # Update password in MongoDB
        
        users_collection.update_one({'_id': ObjectId(session['user_id'])}, {'$set': {'password': new_password}})
        
        flash('Password updated successfully.', 'success')
        return redirect(url_for('mypass'))
        
# PROCEEDING TO FEED PAGE AFTER LOGIN 
@app.route('/main_feed', methods=['POST', 'GET'])
def main_feed():
    user_id = session.get('user_id')
    if user_id:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        datas = list(post_collection.find().sort('post_time', -1))

        if request.method == 'POST':
            current_time = datetime.now()
            post_data = {
                "username": user.get('username'),
                'user_id': user_id,
                'title': request.form['title'],
                'subject': request.form['subject'],
                'description': request.form['description'],
                'links': request.form['links'],
                'post_time': current_time,
            }

            existing_post = post_collection.find_one({
                'user_id': user_id,
                'title': post_data['title'],
                'subject': post_data['subject'],
                'description': post_data['description'],
                'links': post_data['links']
            })

            if existing_post:
                flash('This post already exists.', 'error')
            else:
                post_collection.insert_one(post_data)
                flash('Post added successfully.', 'success')
                return render_template('main_feed.html', datas=datas, user_id1=user_id)
            return render_template('main_feed.html', datas=datas, user_id1=user_id)

        else:
            return render_template('main_feed.html', datas=datas, user_id1=user_id)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login')) 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))    
    
@app.route('/connect')
def connect():
    return render_template('connect_people.html')
# UNDER WORKING  
@app.route('/profile_page')
def dashboard():
    user_data = request.args.get('user_data')
    if user_data:
        user_data = eval(user_data)  
        return render_template('dashboard.html', user_data=user_data)
    else:
        return "User data not found"
    
    
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')