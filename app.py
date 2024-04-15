from flask import Flask, render_template, request, redirect, url_for,jsonify,session,flash
from flask import session
from pymongo import MongoClient
from bson import ObjectId  
from datetime import datetime
import pytz
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
#poll's DATABaSE
client = MongoClient('mongodb://localhost:27017/')
db = client['college_social']
polls_collection = db['polls']

##################################################################################################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017/interests"
mongo = PyMongo(app)

CHOICES = [
      # Club options
    'Drama and Film Club', 'Boat Club', 'Civil Services Aspirants Club',
    'Janeev Club', 'HAM Club', 'Astronomy Club', 'Science Club', 'History Club',
    'Personality Development club', 'Google Student Club', 'Cultural Club',
    'Debate Club', 'Ramanujan Mathematics Club', 'Arts and Crafts', 'Aarya Raas',
    'COEP Philomystics', 'CSAT', 'Robotics Study CLub', 'Aerial Robot Study Circle (ARSC)',
    'Spic Macay', 'CSI', 'DSAI', 'COFSUG', 'COEP Mitra',
    # Sports options
    'Cricket', 'Field Hockey', 'Badminton', 'Football', 'Tennis', 'Kabaddi', 'Wrestling',
    'Table Tennis', 'Basketball', 'Volleyball', 'Athletics', 'Boxing', 'Shooting', 'Chess',
    'Golf', 'Squash', 'Cycling', 'Swimming', 'Martial Arts', 'Archery', 'Snooker', 'Gymnastics',
    'Rowing', 'Rugby', 'Weightlifting', 'Equestrian', 'Polo', 'Billiards', 'Fencing', 'Sailing'
    ,   'Zest-Accounts and Documentation-Head',
    'Zest-Accounts and Documentation-Coordinator',
    'Zest-Accounts and Documentation-Volunteer',
    'Zest-Accounts and Documentation-Ex Coordinator',
    'Zest-Accounts and Documentation-Ex Volunteer',
    'Zest-Accounts and Documentation-Ex Head',
    'Zest-Alumni Outreach Group-Head',
    'Zest-Alumni Outreach Group-Coordinator',
    'Zest-Alumni Outreach Group-Volunteer',
    'Zest-Alumni Outreach Group-Ex Coordinator',
    'Zest-Alumni Outreach Group-Ex Volunteer',
    'Zest-Alumni Outreach Group-Ex Head',
    'Zest-Campus Management-Head',
    'Zest-Campus Management-Coordinator',
    'Zest-Campus Management-Volunteer',
    'Zest-Campus Management-Ex Coordinator',
    'Zest-Campus Management-Ex Volunteer',
    'Zest-Campus Management-Ex Head',
    'Zest-Decor Design and VFX-Head',
    'Zest-Decor Design and VFX-Coordinator',
    'Zest-Decor Design and VFX-Volunteer',
    'Zest-Decor Design and VFX-Ex Coordinator',
    'Zest-Decor Design and VFX-Ex Volunteer',
    'Zest-Decor Design and VFX-Ex Head',
    'Zest-Events and Networking-Head',
    'Zest-Events and Networking-Coordinator',
    'Zest-Events and Networking-Volunteer',
    'Zest-Events and Networking-Ex Coordinator',
    'Zest-Events and Networking-Ex Volunteer',
    'Zest-Events and Networking-Ex Head',
    'Zest-Finance and Marketing-Head',
    'Zest-Finance and Marketing-Coordinator',
    'Zest-Finance and Marketing-Volunteer',
    'Zest-Finance and Marketing-Ex Coordinator',
    'Zest-Finance and Marketing-Ex Volunteer',
    'Zest-Finance and Marketing-Ex Head',
    'Zest-IIC Coordinator-Head',
    'Zest-IIC Coordinator-Coordinator',
    'Zest-IIC Coordinator-Volunteer',
    'Zest-IIC Coordinator-Ex Coordinator',
    'Zest-IIC Coordinator-Ex Volunteer',
    'Zest-IIC Coordinator-Ex Head',
    'Zest-Innovation & Intellectual Property Rights-Head',
    'Zest-Innovation & Intellectual Property Rights-Coordinator',
    'Zest-Innovation & Intellectual Property Rights-Volunteer',
    'Zest-Innovation & Intellectual Property Rights-Ex Coordinator',
    'Zest-Innovation & Intellectual Property Rights-Ex Volunteer',
    'Zest-Innovation & Intellectual Property Rights-Ex Head',
    'Zest-Investor Relations-Head',
    'Zest-Investor Relations-Coordinator',
    'Zest-Investor Relations-Volunteer',
    'Zest-Investor Relations-Ex Coordinator',
    'Zest-Investor Relations-Ex Volunteer',
    'Zest-Investor Relations-Ex Head',
    'Zest-Media and Photography-Head',
    'Zest-Media and Photography-Coordinator',
    'Zest-Media and Photography-Volunteer',
    'Zest-Media and Photography-Ex Coordinator',
    'Zest-Media and Photography-Ex Volunteer',
    'Zest-Media and Photography-Ex Head',
    'Zest-Operations and Logistics-Head',
    'Zest-Operations and Logistics-Coordinator',
    'Zest-Operations and Logistics-Volunteer',
    'Zest-Operations and Logistics-Ex Coordinator',
    'Zest-Operations and Logistics-Ex Volunteer',
    'Zest-Operations and Logistics-Ex Head',
    'Zest-Public Relations-Head',
    'Zest-Public Relations-Coordinator',
    'Zest-Public Relations-Volunteer',
    'Zest-Public Relations-Ex Coordinator',
    'Zest-Public Relations-Ex Volunteer',
    'Zest-Public Relations-Ex Head',
    'Zest-Publicity-Head',
    'Zest-Publicity-Coordinator',
    'Zest-Publicity-Volunteer',
    'Zest-Publicity-Ex Coordinator',
    'Zest-Publicity-Ex Volunteer',
    'Zest-Publicity-Ex Head',
    'Zest-WEB-Head',
    'Zest-WEB-Coordinator',
    'Zest-WEB-Volunteer',
    'Zest-WEB-Ex Coordinator',
    'Zest-WEB-Ex Volunteer',
    'Zest-WEB-Ex Head',
    'Regatta-Accounts and Documentation-Head',
    'Regatta-Accounts and Documentation-Coordinator',
    'Regatta-Accounts and Documentation-Volunteer',
    'Regatta-Accounts and Documentation-Ex Coordinator',
    'Regatta-Accounts and Documentation-Ex Volunteer',
    'Regatta-Accounts and Documentation-Ex Head',
    'Regatta-Alumni Outreach Group-Head',
    'Regatta-Alumni Outreach Group-Coordinator',
    'Regatta-Alumni Outreach Group-Volunteer',
    'Regatta-Alumni Outreach Group-Ex Coordinator',
    'Regatta-Alumni Outreach Group-Ex Volunteer',
    'Regatta-Alumni Outreach Group-Ex Head',
    'Regatta-Campus Management-Head',
    'Regatta-Campus Management-Coordinator',
    'Regatta-Campus Management-Volunteer',
    'Regatta-Campus Management-Ex Coordinator',
    'Regatta-Campus Management-Ex Volunteer',
    'Regatta-Campus Management-Ex Head',
    'Regatta-Decor Design and VFX-Head',
    'Regatta-Decor Design and VFX-Coordinator',
    'Regatta-Decor Design and VFX-Volunteer',
    'Regatta-Decor Design and VFX-Ex Coordinator',
    'Regatta-Decor Design and VFX-Ex Volunteer',
    'Regatta-Decor Design and VFX-Ex Head',
    'Regatta-Events and Networking-Head',
    'Regatta-Events and Networking-Coordinator',
    'Regatta-Events and Networking-Volunteer',
    'Regatta-Events and Networking-Ex Coordinator',
    'Regatta-Events and Networking-Ex Volunteer',
    'Regatta-Events and Networking-Ex Head',
    'Regatta-Finance and Marketing-Head',
    'Regatta-Finance and Marketing-Coordinator',
    'Regatta-Finance and Marketing-Volunteer',
    'Regatta-Finance and Marketing-Ex Coordinator',
    'Regatta-Finance and Marketing-Ex Volunteer',
    'Regatta-Finance and Marketing-Ex Head',
    'Regatta-IIC Coordinator-Head',
    'Regatta-IIC Coordinator-Coordinator',
    'Regatta-IIC Coordinator-Volunteer',
    'Regatta-IIC Coordinator-Ex Coordinator',
    'Regatta-IIC Coordinator-Ex Volunteer',
    'Regatta-IIC Coordinator-Ex Head',
    'Regatta-Innovation & Intellectual Property Rights-Head',
    'Regatta-Innovation & Intellectual Property Rights-Coordinator',
    'Regatta-Innovation & Intellectual Property Rights-Volunteer',
    'Regatta-Innovation & Intellectual Property Rights-Ex Coordinator',
    'Regatta-Innovation & Intellectual Property Rights-Ex Volunteer',
    'Regatta-Innovation & Intellectual Property Rights-Ex Head',
    'Regatta-Investor Relations-Head',
    'Regatta-Investor Relations-Coordinator',
    'Regatta-Investor Relations-Volunteer',
    'Regatta-Investor Relations-Ex Coordinator',
    'Regatta-Investor Relations-Ex Volunteer',
    'Regatta-Investor Relations-Ex Head',
    'Regatta-Media and Photography-Head',
    'Regatta-Media and Photography-Coordinator',
    'Regatta-Media and Photography-Volunteer',
    'Regatta-Media and Photography-Ex Coordinator',
    'Regatta-Media and Photography-Ex Volunteer',
    'Regatta-Media and Photography-Ex Head',
    'Regatta-Operations and Logistics-Head',
    'Regatta-Operations and Logistics-Coordinator',
    'Regatta-Operations and Logistics-Volunteer',
    'Regatta-Operations and Logistics-Ex Coordinator',
    'Regatta-Operations and Logistics-Ex Volunteer',
    'Regatta-Operations and Logistics-Ex Head',
    'Regatta-Public Relations-Head',
    'Regatta-Public Relations-Coordinator',
    'Regatta-Public Relations-Volunteer',
    'Regatta-Public Relations-Ex Coordinator',
    'Regatta-Public Relations-Ex Volunteer',
    'Regatta-Public Relations-Ex Head',
    'Regatta-Publicity-Head',
    'Regatta-Publicity-Coordinator',
    'Regatta-Publicity-Volunteer',
    'Regatta-Publicity-Ex Coordinator',
    'Regatta-Publicity-Ex Volunteer',
    'Regatta-Publicity-Ex Head',
    'Regatta-WEB-Head',
    'Regatta-WEB-Coordinator',
    'Regatta-WEB-Volunteer',
    'Regatta-WEB-Ex Coordinator',
    'Regatta-WEB-Ex Volunteer',
    'Regatta-WEB-Ex Head',
    'Mindspark-Accounts and Documentation-Head',
    'Mindspark-Accounts and Documentation-Coordinator',
    'Mindspark-Accounts and Documentation-Volunteer',
    'Mindspark-Accounts and Documentation-Ex Coordinator',
    'Mindspark-Accounts and Documentation-Ex Volunteer',
    'Mindspark-Accounts and Documentation-Ex Head',
    'Mindspark-Alumni Outreach Group-Head',
    'Mindspark-Alumni Outreach Group-Coordinator',
    'Mindspark-Alumni Outreach Group-Volunteer',
    'Mindspark-Alumni Outreach Group-Ex Coordinator',
    'Mindspark-Alumni Outreach Group-Ex Volunteer',
    'Mindspark-Alumni Outreach Group-Ex Head',
    'Mindspark-Campus Management-Head',
    'Mindspark-Campus Management-Coordinator',
    'Mindspark-Campus Management-Volunteer',
    'Mindspark-Campus Management-Ex Coordinator',
    'Mindspark-Campus Management-Ex Volunteer',
    'Mindspark-Campus Management-Ex Head',
    'Mindspark-Decor Design and VFX-Head',
    'Mindspark-Decor Design and VFX-Coordinator',
    'Mindspark-Decor Design and VFX-Volunteer',
    'Mindspark-Decor Design and VFX-Ex Coordinator',
    'Mindspark-Decor Design and VFX-Ex Volunteer',
    'Mindspark-Decor Design and VFX-Ex Head',
    'Mindspark-Events and Networking-Head',
    'Mindspark-Events and Networking-Coordinator',
    'Mindspark-Events and Networking-Volunteer',
    'Mindspark-Events and Networking-Ex Coordinator',
    'Mindspark-Events and Networking-Ex Volunteer',
    'Mindspark-Events and Networking-Ex Head',
    'Mindspark-Finance and Marketing-Head',
    'Mindspark-Finance and Marketing-Coordinator',
    'Mindspark-Finance and Marketing-Volunteer',
    'Mindspark-Finance and Marketing-Ex Coordinator',
    'Mindspark-Finance and Marketing-Ex Volunteer',
    'Mindspark-Finance and Marketing-Ex Head',
    'Mindspark-IIC Coordinator-Head',
    'Mindspark-IIC Coordinator-Coordinator',
    'Mindspark-IIC Coordinator-Volunteer',
    'Mindspark-IIC Coordinator-Ex Coordinator',
    'Mindspark-IIC Coordinator-Ex Volunteer',
    'Mindspark-IIC Coordinator-Ex Head',
    'Mindspark-Innovation & Intellectual Property Rights-Head',
    'Mindspark-Innovation & Intellectual Property Rights-Coordinator',
    'Mindspark-Innovation & Intellectual Property Rights-Volunteer',
    'Mindspark-Innovation & Intellectual Property Rights-Ex Coordinator',
    'Mindspark-Innovation & Intellectual Property Rights-Ex Volunteer',
    'Mindspark-Innovation & Intellectual Property Rights-Ex Head',
    'Mindspark-Investor Relations-Head',
    'Mindspark-Investor Relations-Coordinator',
    'Mindspark-Investor Relations-Volunteer',
    'Mindspark-Investor Relations-Ex Coordinator',
    'Mindspark-Investor Relations-Ex Volunteer',
    'Mindspark-Investor Relations-Ex Head',
    'Mindspark-Media and Photography-Head',
    'Mindspark-Media and Photography-Coordinator',
    'Mindspark-Media and Photography-Volunteer',
    'Mindspark-Media and Photography-Ex Coordinator',
    'Mindspark-Media and Photography-Ex Volunteer',
    'Mindspark-Media and Photography-Ex Head',
    'Mindspark-Operations and Logistics-Head',
    'Mindspark-Operations and Logistics-Coordinator',
    'Mindspark-Operations and Logistics-Volunteer',
    'Mindspark-Operations and Logistics-Ex Coordinator',
    'Mindspark-Operations and Logistics-Ex Volunteer',
    'Mindspark-Operations and Logistics-Ex Head',
    'Mindspark-Public Relations-Head',
    'Mindspark-Public Relations-Coordinator',
    'Mindspark-Public Relations-Volunteer',
    'Mindspark-Public Relations-Ex Coordinator',
    'Mindspark-Public Relations-Ex Volunteer',
    'Mindspark-Public Relations-Ex Head',
    'Mindspark-Publicity-Head',
    'Mindspark-Publicity-Coordinator',
    'Mindspark-Publicity-Volunteer',
    'Mindspark-Publicity-Ex Coordinator',
    'Mindspark-Publicity-Ex Volunteer',
    'Mindspark-Publicity-Ex Head',
    'Mindspark-WEB-Head',
    'Mindspark-WEB-Coordinator',
    'Mindspark-WEB-Volunteer',
    'Mindspark-WEB-Ex Coordinator',
    'Mindspark-WEB-Ex Volunteer',
    'Mindspark-WEB-Ex Head',
    'Gathering-Accounts and Documentation-Head',
    'Gathering-Accounts and Documentation-Coordinator',
    'Gathering-Accounts and Documentation-Volunteer',
    'Gathering-Accounts and Documentation-Ex Coordinator',
    'Gathering-Accounts and Documentation-Ex Volunteer',
    'Gathering-Accounts and Documentation-Ex Head',
    'Gathering-Alumni Outreach Group-Head',
    'Gathering-Alumni Outreach Group-Coordinator',
    'Gathering-Alumni Outreach Group-Volunteer',
    'Gathering-Alumni Outreach Group-Ex Coordinator',
    'Gathering-Alumni Outreach Group-Ex Volunteer',
    'Gathering-Alumni Outreach Group-Ex Head',
    'Gathering-Campus Management-Head',
    'Gathering-Campus Management-Coordinator',
    'Gathering-Campus Management-Volunteer',
    'Gathering-Campus Management-Ex Coordinator',
    'Gathering-Campus Management-Ex Volunteer',
    'Gathering-Campus Management-Ex Head',
    'Gathering-Decor Design and VFX-Head',
    'Gathering-Decor Design and VFX-Coordinator',
    'Gathering-Decor Design and VFX-Volunteer',
    'Gathering-Decor Design and VFX-Ex Coordinator',
    'Gathering-Decor Design and VFX-Ex Volunteer',
    'Gathering-Decor Design and VFX-Ex Head',
    'Gathering-Events and Networking-Head',
    'Gathering-Events and Networking-Coordinator',
    'Gathering-Events and Networking-Volunteer',
    'Gathering-Events and Networking-Ex Coordinator',
    'Gathering-Events and Networking-Ex Volunteer',
    'Gathering-Events and Networking-Ex Head',
    'Gathering-Finance and Marketing-Head',
    'Gathering-Finance and Marketing-Coordinator',
    'Gathering-Finance and Marketing-Volunteer',
    'Gathering-Finance and Marketing-Ex Coordinator',
    'Gathering-Finance and Marketing-Ex Volunteer',
    'Gathering-Finance and Marketing-Ex Head',
    'Gathering-IIC Coordinator-Head',
    'Gathering-IIC Coordinator-Coordinator',
    'Gathering-IIC Coordinator-Volunteer',
    'Gathering-IIC Coordinator-Ex Coordinator',
    'Gathering-IIC Coordinator-Ex Volunteer',
    'Gathering-IIC Coordinator-Ex Head',
    'Gathering-Innovation & Intellectual Property Rights-Head',
    'Gathering-Innovation & Intellectual Property Rights-Coordinator',
    'Gathering-Innovation & Intellectual Property Rights-Volunteer',
    'Gathering-Innovation & Intellectual Property Rights-Ex Coordinator',
    'Gathering-Innovation & Intellectual Property Rights-Ex Volunteer',
    'Gathering-Innovation & Intellectual Property Rights-Ex Head',
    'Gathering-Investor Relations-Head',
    'Gathering-Investor Relations-Coordinator',
    'Gathering-Investor Relations-Volunteer',
    'Gathering-Investor Relations-Ex Coordinator',
    'Gathering-Investor Relations-Ex Volunteer',
    'Gathering-Investor Relations-Ex Head',
    'Gathering-Media and Photography-Head',
    'Gathering-Media and Photography-Coordinator',
    'Gathering-Media and Photography-Volunteer',
    'Gathering-Media and Photography-Ex Coordinator',
    'Gathering-Media and Photography-Ex Volunteer',
    'Gathering-Media and Photography-Ex Head',
    'Gathering-Operations and Logistics-Head',
    'Gathering-Operations and Logistics-Coordinator',
    'Gathering-Operations and Logistics-Volunteer',
    'Gathering-Operations and Logistics-Ex Coordinator',
    'Gathering-Operations and Logistics-Ex Volunteer',
    'Gathering-Operations and Logistics-Ex Head',
    'Gathering-Public Relations-Head',
    'Gathering-Public Relations-Coordinator',
    'Gathering-Public Relations-Volunteer',
    'Gathering-Public Relations-Ex Coordinator',
    'Gathering-Public Relations-Ex Volunteer',
    'Gathering-Public Relations-Ex Head',
    'Gathering-Publicity-Head',
    'Gathering-Publicity-Coordinator',
    'Gathering-Publicity-Volunteer',
    'Gathering-Publicity-Ex Coordinator',
    'Gathering-Publicity-Ex Volunteer',
    'Gathering-Publicity-Ex Head',
    'Gathering-WEB-Head',
    'Gathering-WEB-Coordinator',
    'Gathering-WEB-Volunteer',
    'Gathering-WEB-Ex Coordinator',
    'Gathering-WEB-Ex Volunteer',
    'Gathering-WEB-Ex Head',
    'PSF-Accounts and Documentation-Head',
    'PSF-Accounts and Documentation-Coordinator',
    'PSF-Accounts and Documentation-Volunteer',
    'PSF-Accounts and Documentation-Ex Coordinator',
    'PSF-Accounts and Documentation-Ex Volunteer',
    'PSF-Accounts and Documentation-Ex Head',
    'PSF-Alumni Outreach Group-Head',
    'PSF-Alumni Outreach Group-Coordinator',
    'PSF-Alumni Outreach Group-Volunteer',
    'PSF-Alumni Outreach Group-Ex Coordinator',
    'PSF-Alumni Outreach Group-Ex Volunteer',
    'PSF-Alumni Outreach Group-Ex Head',
    'PSF-Campus Management-Head',
    'PSF-Campus Management-Coordinator',
    'PSF-Campus Management-Volunteer',
    'PSF-Campus Management-Ex Coordinator',
    'PSF-Campus Management-Ex Volunteer',
    'PSF-Campus Management-Ex Head',
    'PSF-Decor Design and VFX-Head',
    'PSF-Decor Design and VFX-Coordinator',
    'PSF-Decor Design and VFX-Volunteer',
    'PSF-Decor Design and VFX-Ex Coordinator',
    'PSF-Decor Design and VFX-Ex Volunteer',
    'PSF-Decor Design and VFX-Ex Head',
    'PSF-Events and Networking-Head',
    'PSF-Events and Networking-Coordinator',
    'PSF-Events and Networking-Volunteer',
    'PSF-Events and Networking-Ex Coordinator',
    'PSF-Events and Networking-Ex Volunteer',
    'PSF-Events and Networking-Ex Head',
    'PSF-Finance and Marketing-Head',
    'PSF-Finance and Marketing-Coordinator',
    'PSF-Finance and Marketing-Volunteer',
    'PSF-Finance and Marketing-Ex Coordinator',
    'PSF-Finance and Marketing-Ex Volunteer',
    'PSF-Finance and Marketing-Ex Head',
    'PSF-IIC Coordinator-Head',
    'PSF-IIC Coordinator-Coordinator',
    'PSF-IIC Coordinator-Volunteer',
    'PSF-IIC Coordinator-Ex Coordinator',
    'PSF-IIC Coordinator-Ex Volunteer',
    'PSF-IIC Coordinator-Ex Head',
    'PSF-Innovation & Intellectual Property Rights-Head',
    'PSF-Innovation & Intellectual Property Rights-Coordinator',
    'PSF-Innovation & Intellectual Property Rights-Volunteer',
    'PSF-Innovation & Intellectual Property Rights-Ex Coordinator',
    'PSF-Innovation & Intellectual Property Rights-Ex Volunteer',
    'PSF-Innovation & Intellectual Property Rights-Ex Head',
    'PSF-Investor Relations-Head',
    'PSF-Investor Relations-Coordinator',
    'PSF-Investor Relations-Volunteer',
    'PSF-Investor Relations-Ex Coordinator',
    'PSF-Investor Relations-Ex Volunteer',
    'PSF-Investor Relations-Ex Head',
    'PSF-Media and Photography-Head',
    'PSF-Media and Photography-Coordinator',
    'PSF-Media and Photography-Volunteer',
    'PSF-Media and Photography-Ex Coordinator',
    'PSF-Media and Photography-Ex Volunteer',
    'PSF-Media and Photography-Ex Head',
    'PSF-Operations and Logistics-Head',
    'PSF-Operations and Logistics-Coordinator',
    'PSF-Operations and Logistics-Volunteer',
    'PSF-Operations and Logistics-Ex Coordinator',
    'PSF-Operations and Logistics-Ex Volunteer',
    'PSF-Operations and Logistics-Ex Head',
    'PSF-Public Relations-Head',
    'PSF-Public Relations-Coordinator',
    'PSF-Public Relations-Volunteer',
    'PSF-Public Relations-Ex Coordinator',
    'PSF-Public Relations-Ex Volunteer',
    'PSF-Public Relations-Ex Head',
    'PSF-Publicity-Head',
    'PSF-Publicity-Coordinator',
    'PSF-Publicity-Volunteer',
    'PSF-Publicity-Ex Coordinator',
    'PSF-Publicity-Ex Volunteer',
    'PSF-Publicity-Ex Head',
    'PSF-WEB-Head',
    'PSF-WEB-Coordinator',
    'PSF-WEB-Volunteer',
    'PSF-WEB-Ex Coordinator',
    'PSF-WEB-Ex Volunteer',
    'PSF-WEB-Ex Head',
    'Impression-Accounts and Documentation-Head',
    'Impression-Accounts and Documentation-Coordinator',
    'Impression-Accounts and Documentation-Volunteer',
    'Impression-Accounts and Documentation-Ex Coordinator',
    'Impression-Accounts and Documentation-Ex Volunteer',
    'Impression-Accounts and Documentation-Ex Head',
    'Impression-Alumni Outreach Group-Head',
    'Impression-Alumni Outreach Group-Coordinator',
    'Impression-Alumni Outreach Group-Volunteer',
    'Impression-Alumni Outreach Group-Ex Coordinator',
    'Impression-Alumni Outreach Group-Ex Volunteer',
    'Impression-Alumni Outreach Group-Ex Head',
    'Impression-Campus Management-Head',
    'Impression-Campus Management-Coordinator',
    'Impression-Campus Management-Volunteer',
    'Impression-Campus Management-Ex Coordinator',
    'Impression-Campus Management-Ex Volunteer',
    'Impression-Campus Management-Ex Head',
    'Impression-Decor Design and VFX-Head',
    'Impression-Decor Design and VFX-Coordinator',
    'Impression-Decor Design and VFX-Volunteer',
    'Impression-Decor Design and VFX-Ex Coordinator',
    'Impression-Decor Design and VFX-Ex Volunteer',
    'Impression-Decor Design and VFX-Ex Head',
    'Impression-Events and Networking-Head',
    'Impression-Events and Networking-Coordinator',
    'Impression-Events and Networking-Volunteer',
    'Impression-Events and Networking-Ex Coordinator',
    'Impression-Events and Networking-Ex Volunteer',
    'Impression-Events and Networking-Ex Head',
    'Impression-Finance and Marketing-Head',
    'Impression-Finance and Marketing-Coordinator',
    'Impression-Finance and Marketing-Volunteer',
    'Impression-Finance and Marketing-Ex Coordinator',
    'Impression-Finance and Marketing-Ex Volunteer',
    'Impression-Finance and Marketing-Ex Head',
    'Impression-IIC Coordinator-Head',
    'Impression-IIC Coordinator-Coordinator',
    'Impression-IIC Coordinator-Volunteer',
    'Impression-IIC Coordinator-Ex Coordinator',
    'Impression-IIC Coordinator-Ex Volunteer',
    'Impression-IIC Coordinator-Ex Head',
    'Impression-Innovation & Intellectual Property Rights-Head',
    'Impression-Innovation & Intellectual Property Rights-Coordinator',
    'Impression-Innovation & Intellectual Property Rights-Volunteer',
    'Impression-Innovation & Intellectual Property Rights-Ex Coordinator',
    'Impression-Innovation & Intellectual Property Rights-Ex Volunteer',
    'Impression-Innovation & Intellectual Property Rights-Ex Head',
    'Impression-Investor Relations-Head',
    'Impression-Investor Relations-Coordinator',
    'Impression-Investor Relations-Volunteer',
    'Impression-Investor Relations-Ex Coordinator',
    'Impression-Investor Relations-Ex Volunteer',
    'Impression-Investor Relations-Ex Head',
    'Impression-Media and Photography-Head',
    'Impression-Media and Photography-Coordinator',
    'Impression-Media and Photography-Volunteer',
    'Impression-Media and Photography-Ex Coordinator',
    'Impression-Media and Photography-Ex Volunteer',
    'Impression-Media and Photography-Ex Head',
    'Impression-Operations and Logistics-Head',
    'Impression-Operations and Logistics-Coordinator',
    'Impression-Operations and Logistics-Volunteer',
    'Impression-Operations and Logistics-Ex Coordinator',
    'Impression-Operations and Logistics-Ex Volunteer',
    'Impression-Operations and Logistics-Ex Head',
    'Impression-Public Relations-Head',
    'Impression-Public Relations-Coordinator',
    'Impression-Public Relations-Volunteer',
    'Impression-Public Relations-Ex Coordinator',
    'Impression-Public Relations-Ex Volunteer',
    'Impression-Public Relations-Ex Head',
    'Impression-Publicity-Head',
    'Impression-Publicity-Coordinator',
    'Impression-Publicity-Volunteer',
    'Impression-Publicity-Ex Coordinator',
    'Impression-Publicity-Ex Volunteer',
    'Impression-Publicity-Ex Head',
    'Impression-WEB-Head',
    'Impression-WEB-Coordinator',
    'Impression-WEB-Volunteer',
    'Impression-WEB-Ex Coordinator',
    'Impression-WEB-Ex Volunteer',
    'Impression-WEB-Ex Head',
    # Hobbies options
    'Reading', 'Writing', 'Cooking', 'Traveling', 'Photography', 'Painting', 'Gardening', 'Hiking',
    'Playing musical instruments', 'Playing sports', 'Yoga and meditation', 'Watching movies',
    'Gaming', 'Birdwatching', 'Astronomy', 'DIY projects', 'Crafting', 'Knitting or crocheting',
    'Volunteering', 'Learning new languages', 'Collecting stamps', 'Collecting coins', 'Collecting antiques',
    'Fashion and styling', 'Music concerts', 'Music festivals', 'Wine tasting', 'Home decor',
    'Sustainable living practices', 'History', 'Archaeology', 'Fishing', 'Scuba diving', 'Food tasting',
    'Exploring different cuisines', 'Stand-up comedy', 'Tea ceremonies', 'Interior design', 'Camping',
    'Poetry', 'Board games', 'Puzzles', 'Martial arts', 'Writing poetry', 'Writing lyrics', 'Acting',
    'Dancing', 'Singing', 'Motorcycling', 'Beekeeping', 'Robotics', 'Pottery', 'Calligraphy',
    'Paragliding', 'Rock climbing', 'Wine making', 'Horseback riding', 'Target shooting', 'Magic tricks',
    'Origami', 'Sailing', 'Surfing', 'Snowboarding', 'Skiing', 'Rafting', 'Bungee jumping', 'Skateboarding',
    'Longboarding', 'Metal detecting', 'Space exploration', 'Cosplay', 'Cosmetics', 'Makeup tutorials',
    'Hair styling', 'Bodybuilding', 'CrossFit', 'Mountain biking', 'Road cycling', 'Urban exploring',
    'Environmental activism', 'Wildlife photography', 'Animal rescue', 'Pet grooming', 'Dog training',
    'Cat training', 'Horse training', 'Pet adoption', 'Exotic pets', 'Reptiles', 'Amphibians',
    'Marine biology', 'Coral reef conservation', 'Deep-sea diving', 'Underwater photography',
    'Marine conservation', 'Bird photography', 'Bird watching'
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


################################################## TO CONNECT ROUTE ####################################################################

from flask import request

from flask import session

from bson import ObjectId

@app.route('/connect', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        requirements = request.form.getlist('requirement')
        user_requirements = np.array([1 if choice in requirements else 0 for choice in CHOICES])
    else:
        user_requirements = np.zeros(len(CHOICES))

    all_users_interests = []
    all_user_data = []  # Store all user data including username, branch, and year
    all_user_ids = []

    user_id_str = session.get('user_id')  # Assuming session['user_id'] contains the Object ID of the logged-in user
    current_user_id = ObjectId(user_id_str)
    
    for user_data in mongo.db.user_interests.find():
        user_id = user_data['_id']
        all_user_ids.append(user_id)
        
        user_info = users_collection.find_one({'_id': user_id})

        if user_info:
            if user_id == current_user_id:
                continue
            else:
                username = user_info.get('username', 'Unknown')
                branch = user_info.get('branch', 'Unknown')
                year = user_info.get('year', 'Unknown')
        else:
            username, branch, year = 'Unknown', 'Unknown', 'Unknown'

        all_user_data.append({'user_id': user_id, 'username': username, 'branch': branch, 'year': year})
        interests = [user_data[choice] for choice in CHOICES]
        all_users_interests.append(interests)

    # Delete the current user's ID from the list of all user IDs
    index_to_remove = all_user_ids.index(current_user_id)
    del all_user_ids[index_to_remove]

    all_users_interests = np.array(all_users_interests)
    similarities = cosine_similarity([user_requirements], all_users_interests)[0]

    compatible_users_data = [{'user_id': user['user_id'], 'username': user['username'], 'branch': user['branch'], 'year': user['year'], 'similarity': similarity} 
                             for user, similarity in zip(all_user_data, similarities)]
    compatible_users_data.sort(key=lambda x: x['similarity'], reverse=True)

    return render_template('connect_people.html', compatible_users=compatible_users_data)



@app.route('/addpeople', methods=['POST', 'GET'])
def send_request():
    sender_id = session['user_id']
    receiver_id = request.form['user_id']
    # Save connection request in the database
    notification = {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': 'Connection Request',
        'is_read': False,
        'timestamp': datetime.utcnow()
    }
    notifications_collection.insert_one(notification)
    return redirect('/connect')

from flask import render_template
from bson.objectid import ObjectId  # Import this if user_id is stored as ObjectId

@app.route('/notifications')
def notify():
    user_id = session['user_id']
    print(user_id)
    
    # Query unread connection requests for the user
    connection_requests = notifications_collection.find({'receiver_id': user_id, 'is_read': False, 'message': 'Connection Request'})
    
    # Extract sender IDs from the connection requests
    sender_ids = [str(request['sender_id']) for request in connection_requests]  # Assuming sender_id is stored as ObjectId
    
    # Query the users database to get usernames, branches, and years for sender_ids
    user_info = {}
    for sender_id in sender_ids:
        user = users_collection.find_one({'_id': ObjectId(sender_id)})  # Assuming users_collection is your users database collection
        if user:
            user_info[sender_id] = {
                'username': user['username'],
                'branch': user['branch'],
                'year': user['year']
            }
    flash("connection request send")
    
    return render_template('notifications.html', sender_ids=sender_ids, user_info=user_info)



from bson import ObjectId

@app.route('/mark_as_read', methods=['POST'])
def mark_as_read():
    user_id = session['user_id']
    
    # Get the sender_id from the form data
    sender_id = request.form['sender_id']
    
    # Update the document to mark it as read
    notifications_collection.update_one({'receiver_id': user_id, 'sender_id': sender_id, 'is_read': False, 'message': 'Connection Request'}, {'$set': {'is_read': True}})
    
    # Add sender_id to the user's friend list
    users_collection.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'friends': ObjectId(sender_id)}})
    
    # Add user_id to sender's friend list
    users_collection.update_one({'_id': ObjectId(sender_id)}, {'$addToSet': {'friends': ObjectId(user_id)}})
    
    return redirect('/notifications')

@app.route('/myConnections')
def personal():
    user_id = session['user_id']
    
    # Query user's information including friends
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    friends = []
    if user and 'friends' in user:
        friends = users_collection.find({'_id': {'$in': user['friends']}})
    
    return render_template('connection.html', friends=friends)

    
@app.route('/submit', methods=['POST'])
def submit1():
    interests = request.form.getlist('interest')
    user_data = {choice: 0 for choice in CHOICES}
    
    # Get the session ID
    session_id = ObjectId(session.get('user_id'))  # Convert string back to ObjectId
    # print(session_id)

    for interest in interests:
        if interest in CHOICES:
            user_data[interest] = 1
            
    # Add the session ID to user_data
    user_data['_id'] = session_id

    # Insert user_data into the users database
    # mongo.db.users.insert_one(user_data)

    # Also insert user_data into the interests database with the same ObjectId
    mongo.db.user_interests.insert_one(user_data)

    return redirect('/profile')



######################################################  NOTIFICATION PANNEL ################################################################
# @app.route('/Send_notification')
# def notify():
#     return render_template('notifications.html')

# @app.route('/send_request', methods=['POST'])
# def send_request():
#     sender_id = session['user_id']
#     receiver_id = request.form['receiver_id']
#     # Save connection request in the database
#     notification = {
#         'sender_id': sender_id,
#         'receiver_id': receiver_id,
#         'message': 'Connection Request',
#         'is_read': False,
#         'timestamp': datetime.utcnow()
#     }
#     notifications_collection.insert_one(notification)
#     return 'Connection request sent successfully'

# @app.route('/notifications')
# def notifications():
#     user_id = session['user_id']
#     # Query unread notifications for the user
#     notifications = notifications_collection.find({'receiver_id': user_id, 'is_read': False})
#     return render_template('notifications.html', notifications=notifications)



################################################### CONTROL LOGOUT BY TEJAS WORKING  #####################################################
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
######################################## FUNCTION  #########################################################################################   
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
######################################################## INDEX HOME PAGE ###############################################################################
@app.route('/')
def index2():
    return render_template('landing_page.html')
@app.route('/main')
def index1():
    return render_template('Main.html')
######################################################### LOGIN SIGN UP #####################################################################
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

####################################################### PROFILE CREATION OF LOGIN USER ############################################################
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


########################################################### PROFLE PAGE VIEW  AND OTHER #####################################################

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
@app.route('/myprofile', methods=['POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user not logged in
    
    if request.method == 'POST':
        mis_no = request.form['mis_no']
        email = request.form['email']
        mobile_no = request.form['mobile_no']
        # Fetch user data from MongoDB
        user_data = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        # Update user data in MongoDB
        users_collection.update_one({'_id': ObjectId(session['user_id'])}, {'$set': {'email': email, 'MIS_NO': mis_no, 'Mobile_No': mobile_no}})
        
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('myprof'))
@app.route('/myInterest')
def myinter():
    return render_template('interest.html')
    
# @app.route('/myConnections')
# def myconnect():
#     return render_template('connection.html')
##################################################### PASSWORD CHANGE ###################################################################
  
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
        
####################################### PROCEEDING TO FEED PAGE AFTER LOGIN ##############################################################################
@app.route('/main_feed', methods=['POST', 'GET'])
def main_feed():
    user_id = session.get('user_id')
    if user_id:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        datas = list(post_collection.find().sort('post_time', -1))
        return render_template('main_feed.html', datas=datas, user_id1=user_id)
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login')) 
###################################################### CREATE POST HTML #######################################################################################
    
@app.route('/create_post',methods=['POST', 'GET'])
def create_post():
    user_id = session.get('user_id')
    if user_id:
      user = users_collection.find_one({'_id': ObjectId(user_id)})
      datas = list(post_collection.find().sort('post_time', -1))
      if request.method == 'POST':
            time = datetime.utcnow()
            ist=pytz.timezone('Asia/kolkata')
            current_time=time.astimezone(ist)
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
                return redirect(url_for('main_feed'))
                # return render_template('main_feed.html', datas=datas, user_id1=user_id)
      else:
             return render_template('create_post.html')
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('login'))

############################################################## OTHER's PROFILE PAGE #####################################################################
       
@app.route('/dashboard/<user_id1>')
def dashboard1(user_id1):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        try:
            other_user = users_collection.find_one({'_id': ObjectId(user_id1)})
            return render_template('profile_page.html', other_user_data=other_user)
        except Exception as e:
            return f"An error occurred: {str(e)}"
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))    
    
@app.route('/connect')
def connect():
    return render_template('connect_people.html')
######################################################## POLL PAGE   ########################################################################################
@app.route('/pollpage')
def index3():
    user_id = session.get('user_id')
    polls = polls_collection.find()
    return render_template('polls_page.html', polls=polls,userid=user_id)

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
  user_id = session.get('user_id')
  if user_id:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        
        if request.method == 'POST':
         question = request.form['question']
         options = request.form.getlist('option')

        # Insert the new poll into the database
         poll_data = {
            "username": user.get('username'),
            'user_id': user_id,
            'question': question,
            'options': [{ 'option': option, 'votes': 0 } for option in options],
            'polled':[]
        }
         polls_collection.insert_one(poll_data)
         return redirect(url_for('index3'))
        return render_template('create_poll.html')

@app.route('/vote/<poll_id>', methods=['POST'])
def vote(poll_id):
    user_id = session.get('user_id')
    option_index = int(request.form['option'])
    poll = polls_collection.find_one({ '_id': ObjectId(poll_id) })
    
    # Increment the votes for the selected option
    polls_collection.update_one(
        { '_id': ObjectId(poll_id), 'options.option': poll['options'][option_index]['option'] },
        { '$inc': { f'options.{option_index}.votes': 1 } },  
    )
    polls_collection.update_one(
        { '_id': ObjectId(poll_id), 'polled': { '$exists': False } },
        { '$set': { 'polled': [] } }
    )
    polls_collection.update_one(
        { '_id': ObjectId(poll_id) },
        { '$push': { 'polled': user_id } }
    )
    
    return redirect(url_for('index3'))
############################################################# UNDER WORKING  
@app.route('/profile_page')
def dashboard():
    user_data = request.args.get('user_data')
    if user_data:
        user_data = eval(user_data)  
        return render_template('dashboard.html', user_data=user_data)
    else:
        return "User data not found"
    
    
app.secret_key = 'your_secret_key_here'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    
